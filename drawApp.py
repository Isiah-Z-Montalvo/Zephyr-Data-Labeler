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

path = ""
images = []
resizingState = False

def run():
	master = Tk()
	master.title("Zephyr Data Labeler")
	master.geometry("1000x1000")
	
	galleryFrame = LabelFrame(master, text = "Gallery Preview")
	
	def selectFolder():
		global path
		path = askdirectory(title="Select Folder")
		storeImages()
		return
	
	def storeImages():
		global images
		for image in os.listdir(path):
			if ((image.endswith(".jpg")) or 
				(image.endswith(".jpeg")) or 
				(image.endswith(".png"))):
				fullPath = path + "/" + image
				images.append(fullPath)
		galleryPreview()
		return
	
	def galleryPreview():
		r = 0
		c = 0
		galleryFrame.grid(row = 0, column = 0, padx = 20, pady = 20)
		for img in images:
			pic = Image.open(img)
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
	
	def resizeGallery(event):
		global resizingState
		r = 0
		c = 0
		if not resizingState:
			resizingState = True
			for label in galleryFrame.winfo_children():
				label.grid(row = r, column = c, padx = 5)
				c += 1
				master.update()
				if c == math.floor(master.winfo_width() / label.winfo_width()):
					c = 0
					r += 1
			resizingState = False
		return
	
	menuBar = Menu(master)
	fileMenu = Menu(menuBar, tearoff = 0)
	menuBar.add_cascade(label ='File', menu = fileMenu)
	fileMenu.add_command(label ='Open Folder', command = selectFolder)
	
	master.config(menu = menuBar)
	
	master.bind("<Configure>", resizeGallery)
	
	# mainloop, runs infinitely
	mainloop()