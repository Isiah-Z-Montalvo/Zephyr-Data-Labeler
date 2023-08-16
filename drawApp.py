# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
import math
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from PIL import *
from PIL import Image, ImageTk
import os
from os import listdir

def run():
	master = Tk()
	master.title("Zephyr Data Labeler")
	master.geometry("1000x1000")
	
	def selectFolder():
		path = askdirectory(title="Select Folder")
		storeImages(path)
		return
	
	def storeImages(path):
		images = []
		for image in os.listdir(path):
			if (image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".png")):
				images.append(image)
		galleryPreview(path, images)
		return
	
	def galleryPreview(path, images):
		r = 0
		c = 0
		galleryFrame = LabelFrame(master, text = "Gallery Preview")
		galleryFrame.grid(row = 0, column = 0, padx = 20, pady = 20)
		for img in images:
			fullPath = path + "/" + img
			pic = Image.open(fullPath)
			picCopy = pic.copy()
			picCopy.thumbnail((200, 200))
			picPI = ImageTk.PhotoImage(picCopy)
			
			picLabel = Label(galleryFrame, image = picPI)
			picLabel.image = picPI
			picLabel.grid(row = r, column = c, padx = 5)
			c += 1
			
			master.update()
			if c == math.floor(master.winfo_width() / picLabel.winfo_width()):
				c = 0
				r += 1
		return
	
	menuBar = Menu(master)
	fileMenu = Menu(menuBar, tearoff = 0)
	menuBar.add_cascade(label ='File', menu = fileMenu)
	fileMenu.add_command(label ='Open Folder', command = selectFolder)
	
	master.config(menu = menuBar)
	
	# mainloop, runs infinitely
	mainloop()