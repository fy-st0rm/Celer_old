import threading
import socket
import json
import os
import time


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

		# Tokens
		self.ACCEPTED = "[ACCEPTED]"
		self.REJECTED = "[REJECTED]"
		self.LOGIN = "[LOGIN]"
		self.SIGNUP = "[SIGNUP]"
		self.DISCONNECT = "[DISCONNECT]"
		self.MSG = "[MSG]"
		self.SERVER = "[SERVER]"
		self.NEW_SV = "[NEW_SV]"
		self.JOIN = "[JOIN]"

	# Serialization of clients data
	def __load_data(self):
		with open(os.path.join("clients.json"), "r") as r:
			self.clients = json.load(r)
	
	def __save_data(self):
		with open(os.path.join("clients.json"), "w") as w:
			json.dump(self.clients, w)

	# Client handlers
	def __handle_login(self, conn, addr):
		username = ""

		while True:
			recv_info = conn.recv(self.BUFFER).decode(self.FORMAT)
			tokens = recv_info.split(" ")

			# If the info is from login page
			if tokens[0] == self.LOGIN:
				username = tokens[1].split(":")[1]
				password = tokens[2].split(":")[1]
				
				# Checking for username and password
				if username in self.clients:
					if password == self.clients[username]["password"]:
						conn.send(self.ACCEPTED.encode(self.FORMAT))
						return [True, username]
					else:
						conn.send(self.REJECTED.encode(self.FORMAT))
				else:
					conn.send(self.REJECTED.encode(self.FORMAT))

			# If the info is from signup page
			elif tokens[0] == self.SIGNUP:
				username = tokens[1].split(":")[1]
				password = tokens[2].split(":")[1]

				# Checking if username already doesnt exists
				if username not in self.clients:
					# Saving the clients info
					self.clients.update({username: 
											{
												"password": password,
												"ip": addr[0],
												"sv": []
											}
										})
					self.__save_data()
					conn.send(self.ACCEPTED.encode(self.FORMAT))
					return [True, username]
				else:
					conn.send(self.REJECTED.encode(self.FORMAT))

			# If the app closed
			elif tokens[0] == self.DISCONNECT:
				return [False, username]
	
	# Function to create new server
	def __create_new_sv(self, conn, key, name):
		servers = os.listdir(os.path.join("Servers"))
		if key in servers:
			conn.send(self.REJECTED.encode(self.FORMAT))
		else:
			conn.send(self.ACCEPTED.encode(self.FORMAT))

			os.mkdir(os.path.join(f"Servers/{key}"))
			sv_info = {
					"name": name,
					"mem": []
				}

			# Saving the info
			with open(os.path.join(f"Servers/{key}/sv_info.json"), "w") as w:
				json.dump(sv_info, w)

	# Function to send the joined servers' data
	def __send_server_data(self, conn, username):
		servers = self.clients[username]["sv"]
		total_servers = os.listdir(os.path.join("Servers"))

		data_to_send = self.SERVER

		for i in servers:
			for j in total_servers:
				if i == j:
					# Getting server infos
					with open(os.path.join(f"Servers/{j}/sv_info.json"), "r") as r:
						sv_info = json.load(r)
					r.close()
				
					name = sv_info["name"]
					key = j

					data_to_send += f" {key}:{name}"

		conn.send(data_to_send.encode(self.FORMAT))

	# Function to join in a server
	def __join_to_server(self, key, name):
		self.clients[name]["sv"].append(key)
		self.__save_data()

		with open(os.path.join(f"Servers/{key}/sv_info.json"), "r") as r:
			sv_info = json.load(r)
		
		sv_info["mem"].append(name)
		
		with open(os.path.join(f"Servers/{key}/sv_info.json"), "w") as w:
			json.dump(sv_info, w)

	def __handle_clients(self, conn, addr):	
		# Handle login and signup
		client_online = self.__handle_login(conn, addr)

		# Give the user the required data when they are in home page
		if client_online[0]:
			self.active_clients.update({client_online[1]: conn})
			
			self.__send_server_data(conn, client_online[1])

		# Handle the main client and server data trading
		while client_online[0]:
			recv_info = conn.recv(self.BUFFER).decode(self.FORMAT)
			tokens = recv_info.split(" ")

			if tokens[0] == self.DISCONNECT:
				print(f"{colors.RED}{client_online[1]}: disconnected..{colors.DEFAULT}")
				client_online[0] = False

			# When new server is created
			if tokens[0] == self.NEW_SV:
				key = tokens[1].split(":")[1]
				name = tokens[2].split(":")[1]

				self.__create_new_sv(conn, key, name)
			
			# When member joins a server
			elif tokens[0] == self.JOIN:
				name = tokens[1].split(":")[1]
				key = tokens[2].split(":")[1]

				self.__join_to_server(key, name)

				time.sleep(0.5)
				self.__send_server_data(conn, name)

	# Server stuff
	def __create_server(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind(self.ADDR)
		except Exception as e:
			print(f"{colors.RED}{e}{colors.DEFAULT}")

	def start(self):
		print(f"{colors.GREEN}Server is starting....{colors.DEFAULT}")

		self.__create_server()
		self.__load_data()

		self.server.listen()
		while True:
			conn, addr = self.server.accept()
			
			# Creating a new thread
			client_thread = threading.Thread(target = self.__handle_clients, args = (conn, addr, ))
			client_thread.start()


if __name__ == "__main__":
	server = Server()
	server.start()
