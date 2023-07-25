# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory

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

def selectFolder():
	path = askdirectory(title="Select Folder")


def drawWindow():
	# creates a Tk() object
	master = Tk()

	# sets the geometry of main
	# root window
	master.geometry("1000x1000")

	label = Label(master,
				  text ="Zephyr Data Labeler")

	label.pack(pady = 10)

	# a button widget which will open a
	# new window on button click
	btn = Button(master,
				 text ="Open New Window",
				 command = openNewWindow)
	btn.pack(pady = 10)

	# a button widget which will open a
	# new window on button click
	btn2 = Button(master,
				 text ="Select a Folder",
				 command = selectFolder)
	btn2.pack(pady = 10)
	
	# mainloop, runs infinitely
	mainloop()