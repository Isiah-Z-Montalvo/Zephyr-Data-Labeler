# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk
"""
# function to open a new window
# on a button click
def openNewWindow():

	# Toplevel object which will
	# be treated as a new window
	newWindow = Toplevel()

	# sets the title of the
	# Toplevel widget
	newWindow.title("New Window")

	# sets the geometry of toplevel
	newWindow.geometry("200x200")

	# A Label widget to show in toplevel
	Label(newWindow,
		  text ="This is a new window").pack()
"""
def selectFolder():
	path = askdirectory(title="Select Folder")
"""
def drawButton(master, attrs):
	btn = Button(master,
				 image = photoimage,
				 text = attrs[0],
				 command = attrs[1])
	btn.pack(pady = 10)
"""
def drawWindow():
	"""
	btnAttr = {
		"New_Window" : ["Open New Window", openNewWindow],
		"Open_Folder" : ["Select a Folder", selectFolder]
	}
	"""
	# creates a Tk() object
	master = Tk()
	master.title("Zephyr Data Labeler")

	# sets the geometry of main
	# root window
	master.geometry("1000x1000")

	menuBar = Menu(master)
	fileMenu = Menu(menuBar, tearoff = 0)
	menuBar.add_cascade(label ='File', menu = fileMenu)
	fileMenu.add_command(label ='Open Folder', command = selectFolder)

	#drawButton(master, btnAttr["New_Window"])
	#drawButton(master, btnAttr["Open_Folder"])

	master.config(menu = menuBar)
	# mainloop, runs infinitely
	mainloop()