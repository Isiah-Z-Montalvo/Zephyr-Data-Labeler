# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
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
		print(path)
		storeImages(path)
		return
	
	def storeImages(path):
		images = []
		for image in os.listdir(path):
			if (image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".png")):
				images.append(image)
		print(images[0])
		galleryPreview(path, images)
		return
	
	def galleryPreview(path, images):
		for img in images:
			
	
	menuBar = Menu(master)
	fileMenu = Menu(menuBar, tearoff = 0)
	menuBar.add_cascade(label ='File', menu = fileMenu)
	fileMenu.add_command(label ='Open Folder', command = selectFolder)
	
	master.config(menu = menuBar)
	
	# mainloop, runs infinitely
	mainloop()