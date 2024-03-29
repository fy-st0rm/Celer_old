from celer_ui import*
from network import *

# Network constants
IP = socket.gethostbyname("8.tcp.ngrok.io")
PORT = 11874
BUFFER = 1024
FORMAT = "utf-8"

client = Network(IP, PORT, BUFFER, FORMAT)
client.connect()

celer_ui = log_ui(client)
celer_ui.drawUI()
celer_ui.winUI()

# Telling the server that the client is being disconnected
client.send("[DISCONNECT]")

'''
open celer_ui.py and goto line 55 and 58 for values of the username and data!
'''
