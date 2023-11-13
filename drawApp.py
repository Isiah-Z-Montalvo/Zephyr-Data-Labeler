# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
import math
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfile
from tkinter import colorchooser
from PIL import *
from PIL import Image, ImageTk
import os
from os import listdir

path = ""
images = []
resizingState = False
initialState = True

def run():
	master = Tk()
	master.title("Zephyr Data Labeler")
	#master.config(bg="#26242f")
	master.geometry("1000x1000")
	master.state("zoomed")
	style = Style(master)
	
	style.theme_create("DarkenTheSkies", 
					   settings = {
						   "Vertical.TScrollbar": {
							   "configure": {
								   "background": "#26242f"
							   }
						   }
					   })
	
	# Functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def createDataset():
		fileTypes = [("Zephyr Dataset File", "*.zds")]
		file = asksaveasfile(filetypes = fileTypes, defaultextension = fileTypes)
		return
	
	def createClassWidgets():
		classWindow = Toplevel(master)
		classWindow.title("Class Name")
		classWindow.geometry("300x100")
		classNameLabel = Label(classWindow, text = "Enter a Class Name:", font = ("Facon", 16))
		classEntry = Entry(classWindow, width = 20, font = ("Facon", 12))
		
		classNameLabel.grid(row = 0, column = 0, padx = 15, pady = 5)
		classEntry.grid(row = 1, column = 0, pady = 5)
		classWindow.grab_set()
		classWindow.resizable(False, False)
		classWindow.bind("<Return>", lambda event: completeClassEntry(event, classWindow, classEntry))
		return
	
	def completeClassEntry(event, classWindow, classEntry):
		className = classEntry.get()
		classWindow.destroy()
		color = colorchooser.askcolor(title = "Choose Color for %s Class" % (className))
		if color[0] == None:
			return
		r, g, b = color[0]
		classColor = ImageTk.PhotoImage(Image.new("RGBA", (200, 50), (r, g, b, 200)))
		newClass = Button(classFrame, image = classColor, text = className, command = createClassWidgets, compound = "c")
		newClass.image = classColor
		rowNum = 0
		for i in range(len(classFrame.winfo_children()) - 1, -1, -1):
			classFrame.winfo_children()[i].grid(row = rowNum, column = 0, padx = 10, pady = 5, sticky = "w")
			rowNum += 1
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
		galleryPreview()
		return
	
	def createGalleryWidgets():
		galleryContainer = Frame(master)
		galleryCanvas = Canvas(galleryContainer)
		galleryScrollbar = Scrollbar(galleryContainer, orient = "vertical", command = galleryCanvas.yview)
		galleryFrame = LabelFrame(galleryCanvas, text = "Gallery Preview")
		return galleryContainer, galleryCanvas, galleryScrollbar, galleryFrame
	
	def assignGalleryLabels(galleryFrame):
		for img in images:
			pic = Image.open(img)
			picCopy = pic.copy()
			picCopy.thumbnail((200, 200))
			picPI = ImageTk.PhotoImage(picCopy)
			picLabel = Label(galleryFrame, image = picPI)
			picLabel.image = picPI
		return
	
	def renderGallery(galleryFrame, galleryCanvas):
		r = 0
		c = 0
		master.update()
		for label in galleryFrame.winfo_children():
			label.grid(row = r, column = c, padx = 5, pady = 5)
			c += 1
			if c == math.floor(master.winfo_width() / label.winfo_width()):
				c = 0
				r += 1
		galleryCanvas.configure(width = galleryFrame.winfo_width(), height = master.winfo_height() - 100)
		return
	
	def galleryPreview():
		classContainer.grid_remove()
		
		galleryContainer, galleryCanvas, galleryScrollbar, galleryFrame = createGalleryWidgets()
		endGalleryButton = Button(galleryContainer, text = "Confirm", command = lambda: endGallery(galleryContainer))
		assignGalleryLabels(galleryFrame)
		
		galleryCanvas.create_window((0, 0), window = galleryFrame, anchor="nw")
		galleryCanvas.configure(yscrollcommand = galleryScrollbar.set)
		galleryContainer.grid(row = 0, column = 0, padx = 15, pady = 5)
		galleryCanvas.grid(row = 0, column = 0, padx = 15, pady = 5)
		galleryScrollbar.grid(row = 0, column = 1, sticky = "ns")
		endGalleryButton.grid(row = 1, column = 0, ipadx = 50, ipady = 10, pady = 10)
		
		renderGallery(galleryFrame, galleryCanvas)
		master.bind("<Configure>", lambda event: resizeGallery(event, galleryFrame, galleryCanvas))
		galleryFrame.bind("<Configure>", lambda e: galleryCanvas.configure(scrollregion = galleryCanvas.bbox("all")))
		return
	
	def endGallery(galleryContainer):
		galleryContainer.destroy()
		classContainer.grid()
		return
	
	def resizeGallery(event, galleryFrame, galleryCanvas):
		global resizingState
		
		if not resizingState:
			resizingState = True
			if galleryFrame.winfo_exists() and galleryCanvas.winfo_exists(): 
				renderGallery(galleryFrame, galleryCanvas)
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
	logo.thumbnail((210, 210))
	logo = ImageTk.PhotoImage(logo)
	classContainer = Frame(master)
	logoLabel = Label(classContainer, image = logo)
	classLabel = Label(classContainer, text = "Classes", font = ("Facon", 31))
	classCanvas = Canvas(classContainer, highlightthickness = 0)
	classScrollbar = Scrollbar(classContainer, orient = "vertical", command = classCanvas.yview)
	classFrame = Frame(classCanvas)
	classCanvas.create_window((0, 0), window = classFrame, anchor="nw")
	classCanvas.configure(yscrollcommand = classScrollbar.set)
	pixelSize = ImageTk.PhotoImage(Image.new("RGBA", (200, 50)))
	classButton = Button(classFrame, image = pixelSize, text = "Add New Class", command = createClassWidgets, compound = "c")
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
	
	global initialState
	if initialState == True:
		classContainer.grid(row = 0, column = 0, sticky = "w")
		logoLabel.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "w")
		classLabel.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "w")
		classCanvas.grid(row = 2, column = 0, sticky = "w")
		classScrollbar.grid(row = 2, column = 1, sticky = "ns")
		classButton.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "w")
		master.update()
		classCanvas.configure(width = classFrame.winfo_width(), height = master.winfo_height() - 300)
		initialState = False
	
	classFrame.bind("<Configure>", lambda e: classCanvas.configure(scrollregion = classCanvas.bbox("all")))
	#row, column = master.grid_size()
	#master.columnconfigure(column, weight = 1)
	# Form Application - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# mainloop, runs infinitely
	mainloop()