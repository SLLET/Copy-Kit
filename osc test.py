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
