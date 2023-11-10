# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
import math
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfile
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
	#master.config(bg="#26242f")
	master.geometry("1000x1000")
	style = Style(master)
	
	style.theme_create("DarkenTheSkies", 
					   settings = {
						   "Vertical.TScrollbar": {
							   "configure": {
								   "background": "#26242f"
							   }
						   }
					   })
	# Gallery Preview Widgets - - - - - - - - - - - - - - - - - - - - - -
	galleryContainer = Frame(master)
	galleryCanvas = Canvas(galleryContainer)
	galleryScrollbar = Scrollbar(galleryContainer, orient = "vertical", command = galleryCanvas.yview)
	galleryFrame = LabelFrame(galleryCanvas, text = "Gallery Preview")
	# Gallery Preview Widgets - - - - - - - - - - - - - - - - - - - - - -
	
	# Functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def createDataset():
		fileTypes = [("Zephyr Dataset File", "*.zds")]
		file = asksaveasfile(filetypes = fileTypes, defaultextension = fileTypes)
		return
	
	def createClass():
		classWindow = Toplevel(master)
		classWindow.title("Class Name")
		classWindow.geometry("300x100")
		classNameLabel = Label(classWindow, text = "Enter a Class Name:", font = ("Facon", 16))
		classEntry = Entry(classWindow, width = 20, font = ("Facon", 12))
		classNameLabel.grid(row = 0, column = 0, padx = 15, pady = 5)
		classEntry.grid(row = 1, column = 0, pady = 5)
		classWindow.grab_set()
		classWindow.resizable(False, False)
		return
	
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
		galleryCanvas.configure(width = galleryFrame.winfo_width(), height = master.winfo_height() - 150)
		return
	
	def galleryPreview():
		galleryCanvas.create_window((0, 0), window = galleryFrame, anchor="nw")
		galleryCanvas.configure(yscrollcommand = galleryScrollbar.set)
		galleryContainer.grid(row = 0, column = 0, padx = 20, pady = 20)
		galleryCanvas.grid(row = 0, column = 0, padx = 20, pady = 20)
		galleryScrollbar.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "ns")
		renderGallery()
		return
	
	def resizeGallery(event):
		global resizingState
		
		if not resizingState:
			resizingState = True
			renderGallery()
			resizingState = False
		return
	
	def switchLight():
		master.config(bg="white")
		return
	
	def switchDark():
		master.config(bg="#26242f")
		style.theme_use("DarkenTheSkies")
		return
	# Functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Main Page Widgets - - - - - - - - - - - - - - - - - - - - - - - - -
	logo = Image.open("Images/Logo.png")
	logo.thumbnail((200, 200))
	logo = ImageTk.PhotoImage(logo)
	logoLabel = Label(master, image = logo)
	classLabel = Label(master, text = "Classes", font = ("Facon", 28))
	classButton = Button(master, text = "Add New Class", command = createClass)
	# Main Page Widgets - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Form Application - - - - - - - - - - - - - - - - - - - - - - - - - -
	menuBar = Menu(master)
	fileMenu = Menu(menuBar, tearoff = 0)
	themeMenu = Menu(menuBar, tearoff = 0)
	menuBar.add_cascade(label ='File', menu = fileMenu)
	menuBar.add_cascade(label = 'Themes', menu = themeMenu)
	fileMenu.add_command(label ='Open Folder', command = selectFolder)
	fileMenu.add_command(label = "Create New Dataset", command = createDataset)
	themeMenu.add_command(label = "Light", command = switchLight)
	themeMenu.add_command(label = "Dark", command = switchDark)
	
	master.config(menu = menuBar)
	
	master.bind("<Configure>", resizeGallery)
	galleryFrame.bind("<Configure>", lambda e: galleryCanvas.configure(scrollregion = galleryCanvas.bbox("all")))
	
	logoLabel.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "w")
	classLabel.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "w")
	classButton.grid(row = 2, column = 0, ipadx = 50, ipady = 20, padx = 10, pady = 5, sticky = "w")
	
	#row, column = master.grid_size()
	#master.columnconfigure(column, weight = 1)
	# Form Application - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# mainloop, runs infinitely
	mainloop()