import tkinter as tk
import tkinter.font
from tkinter import messagebox
from tkinter import ttk
from tkinter import messagebox
import platform

class main_ui:
	def __init__(self):
		self.window = tk.Tk(className = 'celer')

		#Defining General font
		self.font = tk.font.Font( family = 'Bahnschrift Light', size = 20)

		#Defining stuff
		self.chatEntry = tk.Entry(self.window, width = 60, font = self.font, borderwidth = 0, bg = '#d6d6d6') #Chat text box!
		self.chatDisplay = tk.Text(self.window, width = 60, font = self.font, borderwidth = 1, bg = 'white', relief="solid")
		self.serverList = tk.Listbox(self.window, width = 10, height = 100, borderwidth = 1, relief="solid", font = self.font)
		self.vertical = tk.Scrollbar(self.window, orient = 'vertical')
		self.serverList.config(yscrollcommand = self.vertical.set)
		self.vertical.config(command = self.serverList.yview)
		self.serverSelect = self.serverList.curselection()

		#Checks if enter is pressed
		self.chatEntry.bind('<Return>', self.chatEntryDataGet)

		#Checks for the type of the os for fullscreen
		if platform.system() == "Linux":
			self.window.attributes('-zoomed', True)
		elif platform.system() == "Windows":
			self.window.state("zoomed")


	def drawUI(self):
		self.serverList.pack(side = 'left')
		self.vertical.pack(side = 'left')
		self.chatEntry.pack(side = 'bottom')
		self.chatDisplay.pack(side = 'top')
		self.serverList.insert(1,'ServerName')
	

	def winUI(self):
		self.window.geometry('940x500')
		self.window.wm_minsize(940, 500) #User can resize up to 940,500
		self.window.mainloop()	

	def chatEntryDataGet(self,event):
		self.chatEntryData = self.chatEntry.get() #Puts the data in the variable
		self.chatEntry.delete(0, 'end')#Deletes the data written in entry
		
	
	def startUI(self):
		self.drawUI()
		self.winUI()
		
		
