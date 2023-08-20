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
	
	galleryContainer = Frame(master)
	galleryCanvas = Canvas(galleryContainer)
	galleryScrollbar = Scrollbar(galleryContainer, orient = "vertical", command = galleryCanvas.yview)
	galleryFrame = LabelFrame(galleryCanvas, text = "Gallery Preview")
	
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
				fullPath = os.path.join(path, image)
				images.append(fullPath)
		assignGalleryLabels()
		return
	
	def assignGalleryLabels():
		for img in images:
			pic = Image.open(img)
			picCopy = pic.copy()
			picCopy.thumbnail((200, 200))
			picPI = ImageTk.PhotoImage(picCopy)
			
			picLabel = Label(galleryFrame, image = picPI)
			picLabel.image = picPI
		galleryPreview()
		return
	
	def renderGallery():
		r = 0
		c = 0
		for label in galleryFrame.winfo_children():
			label.grid(row = r, column = c, padx = 5, pady = 5)
			c += 1
			master.update()
			if c == math.floor(master.winfo_width() / label.winfo_width()):
				c = 0
				r += 1
		galleryCanvas.configure(width = galleryFrame.winfo_width(), height = master.winfo_height() - 200)
		return
	
	def galleryPreview():
		galleryCanvas.create_window((0, 0), window = galleryFrame, anchor="nw")
		galleryCanvas.configure(yscrollcommand = galleryScrollbar.set)
		galleryContainer.grid(row = 0, column = 0, padx = 20, pady = 20)
		galleryCanvas.grid(row = 0, column = 0, padx = 20, pady = 20)
		galleryScrollbar.grid(row = 0, column = 1, padx = 20, pady = 20)
		renderGallery()
		return
	
	def resizeGallery(event):
		global resizingState
		
		if not resizingState:
			resizingState = True
			renderGallery()
			resizingState = False
		return
	
	menuBar = Menu(master)
	fileMenu = Menu(menuBar, tearoff = 0)
	menuBar.add_cascade(label ='File', menu = fileMenu)
	fileMenu.add_command(label ='Open Folder', command = selectFolder)
	
	master.config(menu = menuBar)
	
	master.bind("<Configure>", resizeGallery)
	galleryFrame.bind("<Configure>", lambda e: galleryCanvas.configure(scrollregion = galleryCanvas.bbox("all")))
	
	# mainloop, runs infinitely
	mainloop()