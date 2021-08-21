import tkinter as tk
import tkinter.font
from tkinter import messagebox
from tkinter import ttk
from tkinter import messagebox
import platform
import threading
import socket

from encrypt import *


class main_ui:
	def __init__(self, user, network):
		self.window = tk.Tk(className = 'celer')

		# Networking stuff
		self.network = network
		self.running = True
		self.user = user
		self.key = ""

		#Defining General font
		self.font = tk.font.Font( family = 'Bahnschrift Light', size = 20)
		self.font2 = tk.font.Font( family = 'Bahnschrift Light', size = 10)

		#Defining stuff
		self.chatEntry = tk.Entry(self.window, width = 60, font = self.font, borderwidth = 0, bg = 'white')#'#d6d6d6') #Chat text box!
		self.chatDisplay = tk.Text(self.window, width = 60, font = self.font, borderwidth = 1, bg = 'white', relief="solid")
		self.serverList = tk.Listbox(self.window, width = 10, height = 100, borderwidth = 1, relief="solid", font = self.font)
		self.vertical = tk.Scrollbar(self.window, orient = 'vertical')
		self.serverList.config(yscrollcommand = self.vertical.set)
		self.vertical.config(command = self.serverList.yview)
		self.serverSelect = self.serverList.curselection()
		self.serverCreatebutton = tk.Button(text = 'Create Server',command = self.createServer)
		self.serverJoinbutton = tk.Button(text= 'Join Server', command = self.joinServer)

		
		#Checks if enter is pressed
		self.chatEntry.bind('<Return>', self.chatEntryDataGet)

		#Checks if mouse 1 is pressed in the server list
		self.serverList.bind('<1>',self.connectServerselected)

		#Server list number temporary variable
		self.varNum = 0

		#Gets the data of selected item from the list
		self.selectionServer = self.serverList.curselection()

		#Checks for the type of the os for fullscreen
		if platform.system() == "Linux":
			self.window.attributes('-zoomed', True)
		elif platform.system() == "Windows":
			self.window.state("zoomed")		

	def drawUI(self):
		self.serverList.pack(side = 'left')
		self.vertical.pack(side = 'left')
		self.serverCreatebutton.pack(side = 'top')
		self.serverJoinbutton.pack(side= 'top')
		self.chatEntry.pack(side = 'bottom')
		self.chatDisplay.pack(side = 'top')
		self.serverList.insert(1,'ServerNames:')

	def winUI(self):
		self.window.geometry('940x500')
		self.window.wm_minsize(940, 500) #User can resize up to 940,500
		self.window.mainloop()	

	def chatEntryDataGet(self,event):
		self.chatEntryData = self.chatEntry.get() #Puts the data in the variable
		self.chatEntry.delete(0, 'end')#Deletes the data written in entry
			
	def __receiver(self):
		while self.running:
			recv_info = self.network.recv()
			tokens = recv_info.split(" ")

			if tokens[0] == "[DISCONNECT]":
				self.running = False

			elif tokens[0] == "[SERVER]":
				tokens.pop(0)
				self.serverList.delete(1,'end')#Deletes the old list to remove repeating list
				for i in tokens:
					key = i.split(":")[0]
					name = i.split(":")[1]
					self.varNum+=1 #Server's position in the list
					self.serverNames = key+":"+name 
					self.serverList.insert(self.varNum,self.serverNames)#Inserts server list

			# When server creation failed
			elif tokens[0] == "[REJECTED]":
				self.key = self.__create_sv(self.svName)	
				self.__join_sv(self.key)
			elif tokens[0] == "[ACCEPTED]":
				self.__join_sv(self.key)

	def startUI(self):
		recv_thread = threading.Thread(target = self.__receiver)
		recv_thread.start()

		#Starts ui code
		self.drawUI()
		self.winUI()
		
	def createServer(self):
		self.serverCreatewindow = tk.Toplevel(self.window) #Defining new window

		#Defining stuff
		self.serverName = tk.Entry(self.serverCreatewindow,width = 30, font = self.font2, borderwidth = 0, bg = '#d6d6d6' )
		self.serverCreatelabel = tk.Label(self.serverCreatewindow, text = 'Enter the name of the server:', font = self.font2)
		self.serverCreatebutton = tk.Button(self.serverCreatewindow, text = 'Create Server', command = self.revServername)

		#Drawing stuff
		self.serverCreatelabel.place(x=0,y=0)
		self.serverName.place(x=0,y=30)
		self.serverCreatebutton.place( x = 240, y = 30)
		
		#Window property stuff
		self.serverCreatewindow.resizable(False, False)
		self.serverCreatewindow.title("Create Server")
		self.serverCreatewindow.geometry("390x180")	

	def __create_sv(self, name):	
		# Sending the information about the creation of new server
		token = "[NEW_SV]"
		sv_key = generate_key()
		info = f"{token} key:{sv_key} name:{name}"
		self.network.send(info)
		return sv_key

	def __join_sv(self, key):	
		# Joining the sv
		token = "[JOIN]"
		info = f"{token} name:{self.user} key:{key}"
		self.network.send(info)

	def revServername(self):
		self.svName = self.serverName.get()#Server Name data!
		self.key = self.__create_sv(self.svName)
		self.serverCreatewindow.destroy()#Destroys server create window
		tk.messagebox.showinfo("Information", "Server Created!") #Messages user that the server is created!

	def joinServer(self):
		self.serverJoinwindow = tk.Toplevel(self.window) #Defining new window

		#Defining stuff
		self.serverCode = tk.Entry(self.serverJoinwindow,width = 30, font = self.font2, borderwidth = 0, bg = '#d6d6d6' )
		self.serverJoinlabel = tk.Label(self.serverJoinwindow, text = 'Enter the code of the server:', font = self.font2)
		self.serverJoinbutton = tk.Button(self.serverJoinwindow, text = 'Join Server', command = self.revServercode)

		#Drawing stuff
		self.serverJoinlabel.place(x=0,y=0)
		self.serverCode.place(x=0,y=30)
		self.serverJoinbutton.place( x = 240, y = 30)
		
		#Window property stuff
		self.serverJoinwindow.resizable(False, False)
		self.serverJoinwindow.title("Join Server")
		self.serverJoinwindow.geometry("390x180")	

	def revServercode(self):
		self.svCode = self.serverCode.get()#Server code data!	
		print(self.svCode)	

	def connectServerselected(self,event):
		self.selectedServer = self.serverList.get('anchor')#Gets the data from the selected item
		print(self.selectedServer) 
