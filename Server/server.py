import threading
import socket
import json
import os


# Colors for terminal
class colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Server:
	def __init__(self):
		# Server details
		self.IP = socket.gethostbyname(socket.gethostname())
		self.PORT = 5050
		self.BUFFER = 1024
		self.FORMAT = "utf-8"
		self.ADDR = (self.IP, self.PORT)
	
		# Clients 
		self.clients = {}
		self.active_clients = {}

	# Serialization of clients data
	def __load_data(self):
		with open(os.path.join("clients.json"), "r") as r:
			self.clients = json.load(r)
	
	def __save_data(self):
		with open(os.path.join("clients.json"), "w") as w:
			json.dump(self.clients, w)

	# Client handlers
	def __handle_clients(self, conn, addr):
		
		# Handle login and signup

		# Give the user the required data when they are in home page

		# Handle the main client and server data trading

		pass

	# Server stuff
	def __create_server(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind(self.ADDR)
		except Exception as e:
			print(f"{colors.RED}{e}{colors.DEFAULT}")

	def start(self):
		print(f"{colors.GREEN}Server is starting....")

		self.__create_server()
		self.server.listen()
		while True:
			conn, addr = self.server.accept()
			print(addr)


if __name__ == "__main__":
	server = Server()
	server.start()
