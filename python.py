#!/usr/bin/env python

import tkinter as tk
import datetime
import time
from pythonosc import udp_client
from pythonosc import osc_message_builder
from threading import Thread

def now():
    return datetime.datetime.now().astimezone()

scriptstart = now()
file="Logs/"+now().date().isoformat()+" "+now().time().isoformat()[0:8].replace(':','-')+".log"

def pw(*text):
    pout = str(now()) + " "
    with open(file,"a") as f:
        f.write(str(now())+" ")
        for t in text:
            t=str(t)
            f.write(t+" ")
            pout += t + " "
            f.write("\n")
    print(pout)

pw("Script Start")

def blank():
    blank = tk.Tk()
    width,height=1920,1080 # set the variables 
    d=str(width)+"x"+str(height)
    width,height=1920,1080 # set the variables
    blank.geometry(d)
    blank.configure(bg='#000000')
    blank.title("Blank")
    blank.attributes("-fullscreen", True)
    blank.mainloop()

Thread(target=blank).start()

def send_osc(message, address="192.168.2.10", port=53000):
    client = udp_client.SimpleUDPClient(address, port)
    msg = osc_message_builder.OscMessageBuilder(address = message)
    msg = msg.build()
    client.send(msg)

def light():
    pw("Lights Triggered")
    send_osc('/cue/{17}/go')

def alivetime():
    global scriptstart
    delta = now() - scriptstart
    days = delta.days
    hours = int(delta.seconds / 3600)
    minutes = int(delta.seconds / 60) - (hours * 60)
    seconds = delta.seconds - (hours * 3600) - (minutes * 60)
    days = str(days)
    hours = "0" + str(hours)
    minutes = "0" + str(minutes)
    seconds = "0" + str(seconds)
    out = days+":"+hours[-2:]+":"+minutes[-2:]+":"+seconds[-2:]
    return "Uptime: "+out

guess = []
def red():
    guess.append("red")
    pw("Guessed Red")
    pw("Current Guess", guess)

def green():
    guess.append("green")
    pw("Guessed green")
    pw("Current Guess", guess)

def blue():
    guess.append("blue")
    pw("Guessed Blue")
    pw("Current Guess", guess)

def purple():
    guess.append("purple")
    pw("Guessed Purple")
    pw("Current Guess", guess)

def orange():
    guess.append("orange")
    pw("Guessed Orange")
    pw("Current Guess", guess)

def white():
    guess.append("white")
    pw("Guessed White")
    pw("Current Guess", guess)

def win():
        global wint
        pw("Win")
        wint = tk.Label(text=" Congratulations! ",bg="#000000",fg="magenta",font=("Flood std", 90,  'bold'))
        wint2 = tk.Label(text=" It's not Kit, so who is trying to kill Jon? ",bg="#000000",fg="white",font=("Montserrat", 40,  'bold'))
        wint.place(relx=0.5, rely=0.7, anchor='center')
        wint2.place(relx=0.5, rely=0.9, anchor='center')
        infoL.destroy()
        infoR.destroy()
        send_osc('/cue/{18}/go')

def loop():
    if guess[-6:] == ['purple','green','blue','orange','white','red']:
        win()
        return
    else:
        pass
    welcome.after(500,loop)

def runTask():
    global red
    global green
    global blue
    global purple
    global orange
    global white
    global task_window
    global sllet
    global welcome
    global infoL
    global infoR
    global buttons
    global scale
    task_window = tk.Tk()
    width,height=1920,1080 # set the variables 
    d=str(width)+"x"+str(height)+"+3840+0"
    task_window.geometry(d)
    task_window.configure(bg='#000000')
    task_window.title("Copy Kit")

    welcome = tk.Label(text=" Welcome to Copy Kit ",bg="#000000",fg="white",font=("Montserrat", 90,  'bold'))
    welcome.place(relx=0.5, rely=0.25, anchor='center')
    sllet = tk.Label(text=" SLLET ",bg="#000000",fg="magenta",font=("Flood std", 90,  'bold'))
    sllet.place(relx=0.5, rely=0.1, anchor='center')
    infoL = tk.Label(text="Use the clues\nto guess the\ncombination\n\nIt is 6\ncolours long",bg="#000000",fg="white",font=("Arial", 40,  'bold'))
    infoL.place(relx=0.01, rely=0.7, anchor='w')
    infoR = tk.Label(text="The game will\nuse your last\n6 guesses\n\nGood Luck",bg="#000000",fg="white",font=("Arial", 40,  'bold'))
    infoR.place(relx=0.99, rely=0.7, anchor='e')
    buttons = tk.Frame(bg="black")
    scale = 15
    red = tk.Button(buttons, background="red", height=scale, width=2*scale, command=red).grid(row=0,column=0, padx=scale, pady=scale)
    green = tk.Button(buttons, background="green", height=scale, width=2*scale, command=green).grid(row=0,column=1, padx=scale, pady=scale)
    blue = tk.Button(buttons, background="blue", height=scale, width=2*scale, command=blue).grid(row=0,column=2, padx=scale, pady=scale)
    purple = tk.Button(buttons, background="purple", height=scale, width=2*scale, command=purple).grid(row=1,column=0, padx=scale, pady=scale)
    orange = tk.Button(buttons, background="orange", height=scale, width=2*scale, command=orange).grid(row=1,column=1, padx=scale, pady=scale)
    white = tk.Button(buttons, background="white", height=scale, width=2*scale, command=white).grid(row=1,column=2, padx=scale, pady=scale)
    buttons.place(relx=0.5, rely=0.7, anchor='center')

    lights = tk.Button(text="Lights!",bg="#000000",fg="white",font=("Montserrat", 20,  'bold'), command=light)
    lights.place(relx=0.9, rely=0.1, anchor='e')
    
    task_window.attributes("-fullscreen", True)
    loop()
    task_window.mainloop()

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def print_handler(address, *args):
    print(f"{address}: {args}")


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")
    if address == "/task":
        Thread(target=runTask).start()
    
dispatcher = Dispatcher()
dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)

ip = ""
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
print("Ready")
runTask()
#server.serve_forever()  # Blocks forever
print("End")
