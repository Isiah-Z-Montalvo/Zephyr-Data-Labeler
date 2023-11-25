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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

path = ""
classFrequencies = {}
resizingState = False
initialState = True
index = 0
selectedClass = None

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
		newClass = Button(classFrame, image = classColor, text = className, command = lambda: selectClass(newClass), compound = "c")
		newClass.image = classColor
		classFrequencies[newClass] = [0, color[1]]
		global selectedClass
		selectedClass = newClass
		rowNum = 0
		for i in range(len(classFrame.winfo_children()) - 1, -1, -1):
			classFrame.winfo_children()[i].grid(row = rowNum, column = 0, padx = 10, pady = 5, sticky = "w")
			rowNum += 1
		drawPlot()
		return
	
	def selectClass(newClass):
		global selectedClass
		selectedClass = newClass
		return
	
	def selectFolder():
		global path
		path = ""
		path = askdirectory(title="Select Folder")
		if path == "":
			return
		global index
		index = 0
		galleryPreview()
		return
	
	def createGalleryWidgets():
		galleryContainer = Frame(master)
		galleryCanvas = Canvas(galleryContainer)
		galleryScrollbar = Scrollbar(galleryContainer, orient = "vertical", command = galleryCanvas.yview)
		galleryFrame = LabelFrame(galleryCanvas, text = "Gallery Preview")
		return galleryContainer, galleryCanvas, galleryScrollbar, galleryFrame
	
	def assignGalleryLabels(galleryFrame):
		for image in os.listdir(path):
			if ((image.endswith(".jpg")) or 
				(image.endswith(".jpeg")) or 
				(image.endswith(".png"))):
				fullPath = os.path.join(path, image)
			else:
				continue
			pic = Image.open(fullPath)
			pic.thumbnail((200, 200))
			picPI = ImageTk.PhotoImage(pic)
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
			if c == math.floor(galleryCanvas.winfo_width() / label.winfo_width()):
				c = 0
				r += 1
		galleryCanvas.configure(width = master.winfo_width() - 100, height = master.winfo_height() - 100)
		return
	
	def galleryPreview():
		classContainer.grid_remove()
		masterCanvas.grid_remove()
		toolbarContainer.grid_remove()
		
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
		masterCanvas.grid()
		toolbarContainer.grid()
		
		backButton.grid(row = 2, column = 0, pady = 5, sticky = "nw")
		forwButton.grid(row = 2, column = 0, pady = 5, sticky = "ne")
		displayImage()
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
	
	def mainUnbindings():
		imageCanvas.unbind("<ButtonPress-1>")
		imageCanvas.unbind("<B1-Motion>")
		imageCanvas.unbind("<ButtonRelease-1>")
		for bbox in imageCanvas.find_all()[1:]:
			imageCanvas.tag_unbind(bbox, "<Enter>")
			imageCanvas.tag_unbind(bbox, "<Leave>")
		return
	
	def dragState():
		mainUnbindings()
		for bbox in imageCanvas.find_all()[1:]:
			imageCanvas.tag_bind(bbox, "<Enter>", lambda event: enterBbox(event, bbox))
			imageCanvas.tag_bind(bbox, "<Leave>", lambda event: leaveBbox(event))
		return
	
	def enterBbox(event, bbox):
		event.widget.config(cursor = "fleur")
		widget = event.widget.find_withtag("current")[0]
		imageCanvas.move(widget, 100, 100)
		return
	
	def leaveBbox(event):
		event.widget.config(cursor = "arrow")
		return
	
	def resizeState():
		imageCanvas.config(cursor = "sizing")
		return
	
	def zoomState():
		imageCanvas.config(cursor = "plus")
		return
	
	def boundingState():
		mainUnbindings()
		imageCanvas.config(cursor = "arrow")
		imageCanvas.bind("<ButtonPress-1>", lambda event: createBoundingBox(event))
		return
	
	def createBoundingBox(event):
		if classFrequencies:
			initialX = event.x
			initialY = event.y
			bbox = imageCanvas.create_rectangle(initialX, initialY, initialX, initialY, outline = classFrequencies[selectedClass][1], width = 2)
			imageCanvas.bind("<B1-Motion>", lambda event: drawBoundingBox(event, bbox, initialX, initialY))
		return
	
	def drawBoundingBox(event, bbox, initialX, initialY):
		imageCanvas.coords(bbox, initialX, initialY, event.x, event.y)
		imageCanvas.bind('<ButtonRelease-1>', lambda event: endBoundingBox(event))
		return
	
	def endBoundingBox(event):
		classFrequencies[selectedClass][0] += 1
		drawPlot()
		return
	
	def rotateState():
		imageCanvas.config(cursor = "exchange")
		return
	
	def trashState():
		imageCanvas.config(cursor = "pirate")
		return
	
	def drawPlot():
		figure = plt.Figure(figsize = (4.38, 7), dpi = 50)
		axis = figure.add_subplot(111)
		classFrequency = FigureCanvasTkAgg(figure, toolbarContainer)
		cols = ["Frequency", "Color"]
		data = pd.DataFrame.from_dict(classFrequencies, orient = "index", columns = cols)
		axis.set_xticks([])
		axis.yaxis.set_tick_params(labelleft = False)
		data["Frequency"].plot(kind = 'barh', legend = False, ax = axis, color = data["Color"]).bar_label(axis.containers[0], label_type = "center")
		classFrequency.get_tk_widget().grid(row = 1, column = 0, pady = 5, sticky = "nw")
		return
	
	def displayImage():
		global index
		global path
		if index == len(os.listdir(path)) - 1:
			return
		isImage = False
		while isImage == False:
			if ((os.listdir(path)[index].endswith(".jpg")) or 
				(os.listdir(path)[index].endswith(".jpeg")) or 
				(os.listdir(path)[index].endswith(".png"))):
				fullPath = os.path.join(path, os.listdir(path)[index])
				img = Image.open(fullPath)
				img.thumbnail((700, 700))
				img = ImageTk.PhotoImage(img)
				imageCanvas.create_image(0, 0, anchor = NW, image = img)
				imageCanvas.image = img
				imageCanvas.configure(width = img.width(), height = img.height())
				masterCanvas.create_window((masterCanvas.winfo_width()/2, masterCanvas.winfo_height()/2), window = imageCanvas, anchor = "center")
				masterCanvas.update()
				isImage = True
			else: 
				index += 1
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
	classCanvas.create_window((0, 0), window = classFrame, anchor= "nw")
	classCanvas.configure(yscrollcommand = classScrollbar.set)
	pixelSize = ImageTk.PhotoImage(Image.new("RGBA", (200, 50)))
	classButton = Button(classFrame, image = pixelSize, text = "Add New Class", command = createClassWidgets, compound = "c")
	
	masterCanvas = Canvas(master, highlightthickness = 0, bg = "black")
	imageCanvas = Canvas(masterCanvas, highlightthickness = 0)
	
	toolbarContainer = Frame(master)
	toolbarFrame = LabelFrame(toolbarContainer, text = "Toolbar")
	drag = ImageTk.PhotoImage(Image.open("Images/DragIcon.png").resize((92, 92)))
	box = ImageTk.PhotoImage(Image.open("Images/BoundingBoxIcon.png").resize((92, 92)))
	zoom = ImageTk.PhotoImage(Image.open("Images/ZoomIcon.png").resize((92, 92)))
	resize = ImageTk.PhotoImage(Image.open("Images/ResizeIcon.png").resize((92, 92)))
	rotate = ImageTk.PhotoImage(Image.open("Images/RotateIcon.png").resize((92, 92)))
	trash = ImageTk.PhotoImage(Image.open("Images/TrashIcon.png").resize((92, 92)))
	backArr = ImageTk.PhotoImage(Image.open("Images/BackArrow.png").resize((70, 70)))
	forwArr = ImageTk.PhotoImage(Image.open("Images/ForwardArrow.png").resize((70, 70)))
	dragTool = Button(toolbarFrame, image = drag, command = dragState)
	boundingTool = Button(toolbarFrame, image = box, command = boundingState)
	zoomTool = Button(toolbarFrame, image = zoom, command = zoomState)
	resizeTool = Button(toolbarFrame, image = resize, command = resizeState)
	rotateTool = Button(toolbarFrame, image = rotate, command = rotateState)
	trashTool = Button(toolbarFrame, image = trash, command = trashState)
	backButton = Button(toolbarContainer, image = backArr, command = None)
	forwButton = Button(toolbarContainer, image = forwArr, command = None)
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
		
		masterCanvas.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = "nw")
		toolbarContainer.grid(row = 0, column = 2, sticky = "nw")
		toolbarFrame.grid(row = 0, column = 0, sticky = "nw")
		dragTool.grid(row = 0, column = 0, pady = 5)
		boundingTool.grid(row = 1, column = 0, pady = 5)
		zoomTool.grid(row = 2, column = 0, pady = 5)
		resizeTool.grid(row = 0, column = 1, padx = 5, pady = 5)
		rotateTool.grid(row = 1, column = 1, padx = 5, pady = 5)
		trashTool.grid(row = 2, column = 1, padx = 5, pady = 5)
		
		master.update()
		classContainer.update()
		classCanvas.configure(width = classFrame.winfo_width(), height = master.winfo_height() - 300)
		classContainer.update()
		masterCanvas.configure(width = master.winfo_width() - (classContainer.winfo_width() * 2), height = classContainer.winfo_height())
		initialState = False
	
	classFrame.bind("<Configure>", lambda e: classCanvas.configure(scrollregion = classCanvas.bbox("all")))
	#row, column = master.grid_size()
	#master.columnconfigure(column, weight = 1)
	# Form Application - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# mainloop, runs infinitely
	mainloop()