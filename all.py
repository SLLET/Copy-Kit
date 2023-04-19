from threading import Thread
import subprocess
import vlc
import time

def runTask():
    subprocess.run(['python','python.py'])

def runBlank():
    subprocess.run(['python','blank.py'])

Thread(target=runBlank).start()

def runEnd():
    player = vlc.MediaPlayer()
    media = vlc.Media("Scene 3.mp4")
    player.set_media(media)
    player.play()
    player.set_fullscreen(True)

    while player.get_state() != vlc.State.Ended:
        time.sleep(0.5)
    print("Video Done")
    player.release()

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def print_handler(address, *args):
    print(f"{address}: {args}")


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")
    if address == "/task":
        Thread(target=runTask).start()
    elif address == "/end":
        Thread(target=runEnd).start()
    
dispatcher = Dispatcher()
dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)

ip = ""
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
print("Ready")
#runEnd()
#runTask()
server.serve_forever()  # Blocks forever
print("End")

Thread(target=runTask).start()
Thread(target=runBlank).start()
