# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory

def run():
	master = Tk()
	master.title("Zephyr Data Labeler")
	master.geometry("1000x1000")
	
	def selectFolder():
		path = askdirectory(title="Select Folder")
	
	menuBar = Menu(master)
	fileMenu = Menu(menuBar, tearoff = 0)
	menuBar.add_cascade(label ='File', menu = fileMenu)
	fileMenu.add_command(label ='Open Folder', command = selectFolder)
	
	master.config(menu = menuBar)
	
	# mainloop, runs infinitely
	mainloop()