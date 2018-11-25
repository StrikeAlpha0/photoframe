from Tkinter import *
import tkFileDialog
import sys
from subprocess import call
import os
import paramiko
from scp import SCPClient
import subprocess

LARGE_FONT= ("Verdana", 12)

class BaconBits(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs) 
        container = Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix):
            global app
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
        self.show_frame(StartPage)
    

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="PhotoFrame.py", font=LARGE_FONT, fg="sea green")
        label.pack(pady=10,padx=10)

        button = Button(self, text="Upload", command=lambda: controller.show_frame(PageOne))
        button.pack()
        button2 = Button(self, text="Remove", command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        button3 = Button(self, text="Test Connection", command=lambda: controller.show_frame(PageThree))
        button3.pack()
        button4 = Button(self, text="To HDMI", command=lambda: controller.show_frame(PageFour))
        button4.pack()
        button5 = Button(self, text="To LCD", command=lambda: controller.show_frame(PageFive))
        button5.pack()
        button6 = Button(self, text="Exit", command=lambda: controller.show_frame(PageSix))
        button6.pack()

class PageOne(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Upload", font=LARGE_FONT, fg="sea green")
        label.pack(pady=10,padx=10)

        textbox = Entry(self, bd =1)
        textbox.pack()

        button3 = Button(self, text="Browse & Upload", command=lambda: open_something(textbox))
        button3.pack()
        button = Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(StartPage))
        button.pack()

class PageTwo(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Remove", font=LARGE_FONT, fg="sea green")
        label.pack(pady=10,padx=10)

        textbox = Entry(self, bd =1)
        textbox.pack()

        button2 = Button(self, text="Send and Delete", command=lambda: send_something(textbox))
        button2.pack()
        button = Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(StartPage))
        button.pack()

class PageThree(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Test Connection", font=LARGE_FONT, fg="sea green")
        label.pack(pady=10,padx=10)
        
        message = "Unknown!"
        self.textchange = Label(self, text=message, font=LARGE_FONT, fg="black")
        self.textchange.pack(pady=10,padx=10)

        button4 = Button(self, text="Test Connection", command=lambda: ping_it(self, self.textchange))
        button4.pack()

        button = Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(StartPage))
        button.pack()
        button2 = Button(self, text="Send", command=lambda: controller.show_frame(PageOne))
        button2.pack()
        button3 = Button(self, text="Remove", command=lambda: controller.show_frame(PageTwo))
        button3.pack()

class PageFour(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Switch to HDMI", font=LARGE_FONT, fg="black")
        label.pack()

        button = Button(self, text="Yes", fg="red2", command=lambda: to_HDMI())
        button.pack(pady=10,padx=10)
        button2 = Button(self, text="No", command=lambda: controller.show_frame(StartPage))
        button2.pack()

class PageFive(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Switch to LCD", font=LARGE_FONT, fg="black")
        label.pack()

        button = Button(self, text="Yes", fg="red2", command=lambda: to_LCD())
        button.pack(pady=10,padx=10)
        button2 = Button(self, text="No", command=lambda: controller.show_frame(StartPage))
        button2.pack()

class PageSix(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Are you sure you want to Exit?", font=LARGE_FONT, fg="sea green")
        label.pack(pady=10,padx=10)

        button = Button(self, text="Yes", command=sys.exit)
        button.pack()
        button2 = Button(self, text="No", command=lambda: controller.show_frame(StartPage))
        button2.pack()

def ping_it(self,event):
    #hostname = "IP address(string)"
    response = os.system("ping -c 1 " + hostname)

    if response == 0:
        event.config(text="Connected!")
        print hostname, 'is up!'
    else:
        event.config(text="Disconnected!")
        print hostname, 'is down!'

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    #client.set_missing_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def open_something(textbox):
    app.fileName = tkFileDialog.askopenfilename(title = "Select File to Send", filetypes = (("jpeg files", "*.jpg"),("All files", "*.*")))
    print app.fileName
    #ssh = createSSHClient("IP address(string)", port(int), "user(string)", "password of user(string)")
    with SCPClient(ssh.get_transport()) as scp:
        #scp.put(app.fileName, 'full path of directory(string)')
     

def send_something(textbox):
    app.fileName = tkFileDialog.askopenfilename(title = "Select file to send and delete", filetypes = (("jpeg files", "*.jpg"),("All files", "*.*")))
    print app.fileName

def to_LCD():
   os.system("sudo cp ./usr/tft35a-overlay.dtb /boot/overlays/")
   os.system("sudo cp ./usr/tft35a-overlay.dtb /boot/overlays/tft35a.dtbo")
   os.system("sudo cp -rf ./usr/99-calibration.conf-35  /etc/X11/xorg.conf.d/99-calibration.conf")
   os.system("sudo cp -rf ./usr/99-fbturbo.conf  /usr/share/X11/xorg.conf.d/")
   os.system("sudo cp ./usr/inittab /etc/")
   os.system("sudo cp ./config-35.txt /boot/config.txt")
   os.system("reboot")

def to_HDMI():
    os.system("sudo cp -rf ./usr/modules-HDMI  /etc/modules")
    os.system("sudo cp -rf ./usr/99-fbturbo.conf-HDMI  /usr/share/X11/xorg.conf.d/99-fbturbo.conf")
    os.system("sudo cp ./config-normal.txt /boot/config.txt")
    os.system("sudo reboot")

app = BaconBits()
app.title("PhotoFrame.Py")
app.mainloop()

