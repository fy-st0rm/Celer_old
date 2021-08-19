import tkinter as tk
import tkinter.font
from tkinter import messagebox
from tkinter import ttk
from tkinter import messagebox


class log_ui:
	def __init__(self, network):
		self.window = tk.Tk(className = 'celer')
		self.network = network

		#Tabs Setup
		self.notebook = ttk.Notebook(self.window)
		self.tab1 = tk.Frame(self.notebook, width = 490, height = 700, bg = 'grey')
		self.tab2 = tk.Frame(self.notebook, width = 490, height = 700, bg = 'grey')

		#Defining General font
		self.font = tk.font.Font( family = 'Roboto', size = 20)

		#Wigets in tab1
		self.title_signin = tk.Label(self.tab1,text = 'celer\nSign in Window', font = self.font, fg = 'white', bg ='grey')
		self.username_signin = tk.Entry(self.tab1, bg = 'white', width = 20, borderwidth = 0, font = self.font)
		self.password_signin = tk.Entry(self.tab1, bg = 'white', width = 20, borderwidth = 0, font = self.font, show = '*')
		self.button_singnin = tk.Button(self.tab1, text = 'Signin!', command = self.getdataSignin)

		#Wigets in tab2
		self.title_signup = tk.Label(self.tab2,text = 'celer\nSign up Window', font = self.font, fg = 'white', bg ='grey')
		self.username_signup = tk.Entry(self.tab2, bg = 'white', width = 20, borderwidth = 0, font = self.font)
		self.password_signup = tk.Entry(self.tab2, bg = 'white', width = 20, borderwidth = 0, font = self.font, show = '*')
		self.button_singnup = tk.Button(self.tab2, text = 'Signup!', command = self.getdataSignup)		

	def drawUI(self):
		self.notebook.pack()#Drawing notebook

		#Drawing widgets in tab2
		self.title_signin.place(x=0,y=0)
		self.username_signin.place(x=5, y=100, height = 40)
		self.password_signin.place(x = 5, y = 150, height = 40)
		self.button_singnin.place(x=5, y= 200)

		#Drawing widgets in tab2
		self.title_signup.place(x=0,y=0)
		self.username_signup.place(x=5,y=100, height = 40)
		self.password_signup.place(x=5,y=150,height=40)
		self.button_singnup.place(x=5,y=200)

		#Tab drawing stuff
		self.tab1.place(x =0,y=0, anchor = 'center')
		self.tab2.place(x =0,y=0, anchor = 'center')
		self.notebook.add(self.tab1, text = 'Signin')
		self.notebook.add(self.tab2, text = 'Signup')

	def getdataSignin(self):
		username = self.username_signin.get()#Variable for username of Tab1
		password = self.password_signin.get()#Variable for password of Tab1

		token = "[LOGIN]"
		info = f"{token} username:{username} password:{password}"
		self.network.send(info)

		# Reciving the reply from the server
		reply = self.network.recv()
		print(reply)

	def getdataSignup(self):
		username = self.username_signup.get()#Variable for username of Tab2
		password = self.password_signup.get()	#Variable for password of Tab2
		
		token = "[SIGNUP]"
		info = f"{token} username:{username} password:{password}"
		self.network.send(info)

		# Reciving the reply from the server
		reply = self.network.recv()
		print(reply)

	def winUI(self):
		#Window setup
		self.window.geometry('500x600')	
		self.window.resizable(False, False)
		self.window.mainloop()




   
