from pythonosc import udp_client
from pythonosc import osc_message_builder
import time

def send_osc(message, address="192.168.2.10", port=53000):
    client = udp_client.SimpleUDPClient(address, port)
    msg = osc_message_builder.OscMessageBuilder(address = message)
    msg = msg.build()
    client.send(msg)

send_osc('/cue/{11}/go')
time.sleep(5)
send_osc('/cue/{11}/stop')

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def print_handler(address, *args):
    print(f"{address}: {args}")

def default_handler(address, *args):
    print("I go here")
    print(f"DEFAULT {address}: {args}")

dispatcher = Dispatcher()
dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)

ip = ""
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
print("Ready")
server.serve_forever()  # Blocks forever
print("End")
