# Library Imports - - - - - - - - - - - - - - - - - - - - - - - - - -
import math
from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser
from PIL import *
from PIL import Image, ImageTk
import os
from os import listdir
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import json
# Library Imports - - - - - - - - - - - - - - - - - - - - - - - - - -

# Global Variables - - - - - - - - - - - - - - - - - - - - - - - - - -
path = ""
projectPath = ""
projectData = ""
classFrequencies = {}
currentImage = ""
originalImageSize = 0
index = 0
buttonCursors = {"Standard" : "arrow", "Drag" : "fleur", "Resize" : "sizing", "Zoom" : "plus", "Delete" : "pirate"}
resizingState = False
initialState = True
selectedClass = None
openedProject = None
# Global Variables - - - - - - - - - - - - - - - - - - - - - - - - - -

def run():
	# Create Application - - - - - - - - - - - - - - - - - - - - - - - - - -
	master = Tk()
	master.title("Zephyr Data Labeler")
	#master.config(bg="#26242f")
	master.geometry("1000x1000")
	master.state("zoomed")
	# Create Application - - - - - - - - - - - - - - - - - - - - - - - - - -

	# Functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Persistence Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	def createDataset(event, directoryEntry, directoryWindow):
		directoryName = directoryEntry.get()
		directoryWindow.destroy()
		file = askdirectory()
		directoryName = file + "/" + directoryName
		fileName = directoryName.split("/")[-1]
		os.mkdir(directoryName)
		global path, classFrequencies, index, selectedClass, projectData, currentImage, originalImageSize
		projectData = directoryName + "/" + fileName + "Data" + ".txt"
		dataFile = open(projectData, "x")
		dataFile = open(projectData, "w")
		dataFile.write("Image, X, Y, Width, Height, Label\n")
		dataFile.close()
		projectParameters = {
			"projectName" : fileName,
			"imagePath" : path,
			"classFrequencies" : classFrequencies,
			"index" : index,
			"selectedClass" : selectedClass,
			"projectPath" : directoryName + "/",
			"projectData" : projectData,
			"currentImage" : currentImage,
			"originalImageSize" : originalImageSize
		}
		with open(directoryName + "/" + fileName + ".json", "w") as outfile:
			json.dump(projectParameters, outfile)		
		global openedProject
		openedProject = fileName
		return
	
	def openDataset():
		fileTypes = [("Zephyr Dataset File", "*.json")]
		file = askopenfilename(filetypes = fileTypes, defaultextension = fileTypes)
		with open(file, "r") as openfile:
			projectParameters = json.load(openfile)
			global openedProject, path, classFrequencies, index, selectedClass, projectPath, projectData, currentImage, originalImageSize
			openedProject, path, classFrequencies, index, selectedClass, projectPath, projectData, currentImage, originalImageSize = projectParameters.values()
		for key in classFrequencies:
			loadButton(key, classFrequencies[key][2])
		if path != "":
			displayImage()
		if classFrequencies:
			drawPlot()
		return
	
	def saveDataset():
		fileTypes = [("Zephyr Dataset File", "*.json")]
		file = asksaveasfile(filetypes = fileTypes, defaultextension = fileTypes)
		fileName = file.name.split("/")[-1]
		fileName = fileName.split(".")[0]
		global openedProject, path, classFrequencies, index, selectedClass, projectPath, projectData, currentImage, originalImageSize
		if fileName == openedProject:
			projectParameters = {
				"projectName" : openedProject,
				"imagePath" : path,
				"classFrequencies" : classFrequencies,
				"index" : index,
				"selectedClass" : selectedClass,
				"projectPath" : projectPath,
				"projectData" : projectData,
				"currentImage" : currentImage,
				"originalImageSize" : originalImageSize
			}
			serialize = json.dumps(projectParameters)
			with open(file.name, "w") as outfile:
				outfile.write(serialize)
		else:
			print("error")
		return
	
	def nameDirectory():
		directoryWindow = Toplevel(master)
		directoryWindow.title("Directory Name")
		directoryWindow.geometry("350x100")
		directoryNameLabel = Label(directoryWindow, text = "Enter a Directory Name:", font = ("Facon", 16))
		directoryEntry = Entry(directoryWindow, width = 20, font = ("Facon", 12))
		
		directoryNameLabel.grid(row = 0, column = 0, padx = 15, pady = 5)
		directoryEntry.grid(row = 1, column = 0, pady = 5)
		directoryWindow.grab_set()
		directoryWindow.resizable(False, False)
		directoryWindow.bind("<Return>", lambda event: createDataset(event, directoryEntry, directoryWindow))
		return
	# Persistence Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
		
	# CLass Creation Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
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
		loadButton(className, color[0])
		classFrequencies[className] = [0, color[1], color[0]]
		global selectedClass
		selectedClass = className
		drawPlot()
		return
	
	def loadButton(className, rgb):
		r, g, b = rgb
		classColor = ImageTk.PhotoImage(Image.new("RGBA", (200, 50), (r, g, b, 200)))
		newClass = Button(classFrame, image = classColor, text = className, command = lambda: selectClass(className), compound = "c")
		newClass.image = classColor
		rowNum = 0
		for i in range(len(classFrame.winfo_children()) - 1, -1, -1):
			classFrame.winfo_children()[i].grid(row = rowNum, column = 0, padx = 10, pady = 5, sticky = "w")
			rowNum += 1
		return
	
	def selectClass(className):
		global selectedClass
		selectedClass = className
		return
	# CLass Creation Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Gallery Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
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
		count = 0
		for image in os.listdir(path):
			if ((image.endswith(".jpg")) or 
				(image.endswith(".jpeg")) or 
				(image.endswith(".png"))):
				fullPath = os.path.join(path, image)
				count += 1
			else:
				continue
			pic = Image.open(fullPath)
			pic.thumbnail((200, 200))
			picPI = ImageTk.PhotoImage(pic)
			picLabel = Label(galleryFrame, image = picPI)
			picLabel.image = picPI
			if count >= 100:
				break
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
	# Gallery Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# State/Tool Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	# Drag Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	def mainUnbindings():
		imageCanvas.config(cursor = buttonCursors["Standard"])
		imageCanvas.unbind("<ButtonPress-1>")
		imageCanvas.unbind("<B1-Motion>")
		imageCanvas.unbind("<ButtonRelease-1>")
		for bbox in imageCanvas.find_all()[1:]:
			imageCanvas.tag_unbind(bbox, "<Enter>")
			imageCanvas.tag_unbind(bbox, "<ButtonPress-1>")
			imageCanvas.tag_unbind(bbox, "<B1-Motion>")
			imageCanvas.tag_unbind(bbox, "<Leave>")
		return
	
	def dragState():
		mainUnbindings()
		for bbox in imageCanvas.find_all()[1:]:
			imageCanvas.tag_bind(bbox, "<Enter>", lambda event: enterBbox(event, "Drag"))
			imageCanvas.tag_bind(bbox, "<ButtonPress-1>", lambda event: bboxCoords(event))
			imageCanvas.tag_bind(bbox, "<Leave>", lambda event: leaveBbox(event, "Standard"))
		return
	
	def enterBbox(event, state):
		event.widget.config(cursor = buttonCursors[state])
		return
	
	def bboxCoords(event):
		widget = event.widget.find_withtag("current")[0]
		x, y, width, height = imageCanvas.coords(widget)
		width = width - x
		height = height - y
		imageCanvas.tag_bind(widget, "<B1-Motion>", lambda event: moveBbox(event, x, y, width, height))
		return
	
	def moveBbox(event, x, y, width, height):
		widget = event.widget.find_withtag("current")[0]
		imageCanvas.coords(widget, event.x, event.y, width + event.x, height + event.y)
		return
	
	def leaveBbox(event, state):
		event.widget.config(cursor = buttonCursors[state])
		return
	# Drag Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Resize Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	def resizeState():
		mainUnbindings()
		for bbox in imageCanvas.find_all()[1:]:
			imageCanvas.tag_bind(bbox, "<Enter>", lambda event: enterBbox(event, "Resize"))
			imageCanvas.tag_bind(bbox, "<ButtonPress-1>", lambda event: getResizeCoords(event))
			imageCanvas.tag_bind(bbox, "<Leave>", lambda event: leaveBbox(event, "Standard"))
		return
	
	def getResizeCoords(event):
		widget = event.widget.find_withtag("current")[0]
		initialX, initialY = imageCanvas.coords(widget)[:2]
		imageCanvas.tag_bind(widget, "<B1-Motion>", lambda event: resizeBbox(event, initialX, initialY))
		return
	
	def resizeBbox(event, initialX, initialY):
		widget = event.widget.find_withtag("current")[0]
		imageCanvas.coords(widget, initialX, initialY, event.x, event.y)
		return
	# Resize Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Zoom Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	def zoomState():
		mainUnbindings()
		imageCanvas.config(cursor = buttonCursors["Zoom"])
		imageCanvas.bind("<ButtonPress-1>", lambda event: zoomCanvas(event))
		return
	
	def zoomCanvas(event):
		bboxes = []
		for bbox in imageCanvas.find_all()[1:]:
			bboxes.append(imageCanvas.coords(bbox))
		
		imageCanvas.delete("all")
		masterCanvas.delete("all")
		
		scalingWeight = 100 / imageCanvas.winfo_width()
		scalingWeight += 1
		displayImage(width = imageCanvas.winfo_width() + 100, height = imageCanvas.winfo_height() + 100)
		for bbox in bboxes:
			imageCanvas.create_rectangle(bbox[0] * scalingWeight, bbox[1] * scalingWeight, bbox[2] * scalingWeight, bbox[3] * scalingWeight, outline = classFrequencies[selectedClass][1], width = 2, tags = selectedClass)
		return
	
	def zoomOutState():
		mainUnbindings()
		imageCanvas.config(cursor =  buttonCursors["Zoom"])
		imageCanvas.bind("<ButtonPress-1>", lambda event: zoomOutImage(event))
		return
	
	def zoomOutImage(event):
		bboxes = []
		for bbox in imageCanvas.find_all()[1:]:
			bboxes.append(imageCanvas.coords(bbox))
		
		imageCanvas.delete("all")
		masterCanvas.delete("all")
		
		scalingWeight = 100 / imageCanvas.winfo_width()
		scalingWeight = 1 - scalingWeight
		displayImage(width = imageCanvas.winfo_width() - 100, height = imageCanvas.winfo_height() - 100)
		for bbox in bboxes:
			imageCanvas.create_rectangle(bbox[0] * scalingWeight, bbox[1] * scalingWeight, bbox[2] * scalingWeight, bbox[3] * scalingWeight, outline = classFrequencies[selectedClass][1], width = 2, tags = selectedClass)
		return
	# Zoom Functions - - - - - - - - - - - - - - - - - - - - - - - - - -

	# Bounding Box Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	def boundingState():
		mainUnbindings()
		imageCanvas.config(cursor = "arrow")
		imageCanvas.bind("<ButtonPress-1>", lambda event: createBoundingBox(event))
		return
	
	def createBoundingBox(event):
		if classFrequencies:
			initialX = event.x
			initialY = event.y
			bbox = imageCanvas.create_rectangle(initialX, initialY, initialX, initialY, outline = classFrequencies[selectedClass][1], width = 2, tags = selectedClass)
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
	# Bounding Box Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Trash Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	def trashState():
		mainUnbindings()
		for bbox in imageCanvas.find_all()[1:]:
			imageCanvas.tag_bind(bbox, "<Enter>", lambda event: enterBbox(event, "Delete"))
			imageCanvas.tag_bind(bbox, "<ButtonPress-1>", lambda event: deleteBbox(event, "Standard"))
			imageCanvas.tag_bind(bbox, "<Leave>", lambda event: leaveBbox(event, "Standard"))
		return
	
	def deleteBbox(event, state):
		widget = event.widget.find_withtag("current")[0]
		classFrequencies[imageCanvas.itemcget(widget, "tags").split()[0]][0] -= 1
		imageCanvas.delete(widget)
		drawPlot()
		imageCanvas.config(cursor = buttonCursors[state])
		return
	# Trash Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	# State/Tool Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Display Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	def drawPlot():
		figure = plt.Figure(figsize = (4.38, 7), dpi = 50)
		axis = figure.add_subplot(111)
		classFrequency = FigureCanvasTkAgg(figure, toolbarContainer)
		cols = ["Frequency", "Color", "RGB"]
		data = pd.DataFrame.from_dict(classFrequencies, orient = "index", columns = cols)
		axis.set_xticks([])
		axis.yaxis.set_tick_params(labelleft = False)
		data["Frequency"].plot(kind = 'barh', legend = False, ax = axis, color = data["Color"]).bar_label(axis.containers[0], label_type = "center")
		classFrequency.get_tk_widget().grid(row = 1, column = 0, pady = 5, sticky = "nw")
		return
	
	def displayImage(width = 500, height = 500):
		global index, path, currentImage, originalImageSize
		isImage = False
		while isImage == False:
			if ((os.listdir(path)[index].endswith(".jpg")) or 
				(os.listdir(path)[index].endswith(".jpeg")) or 
				(os.listdir(path)[index].endswith(".png"))):
				currentImage = os.listdir(path)[index]
				fullPath = os.path.join(path, currentImage)
				img = Image.open(fullPath)
				originalImageSize = img.size[0]
				img = img.resize((width, height))
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
	
	def goBack():
		global index
		if index == 0:
			return
		imageCanvas.delete("all")
		masterCanvas.delete("all")
		index -= 1
		displayImage()
		return
	
	def goForward():
		global index
		if index == len(os.listdir(path)) - 1:
			return
		imageCanvas.delete("all")
		masterCanvas.delete("all")
		index += 1
		displayImage()
		return
	# Display Functions - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	def exportBoundingBoxes():
		global currentImage, projectData, originalImageSize
		resizeDifference = imageCanvas.winfo_width() - originalImageSize
		scalingWeight = resizeDifference / imageCanvas.winfo_width()
		scalingWeight = 1 - scalingWeight
		dataFile = open(projectData, "a")
		for bbox in imageCanvas.find_all()[1:]:
			dataString = currentImage
			label = imageCanvas.gettags(bbox)[0]
			x, y, width, height = tuple([x * scalingWeight for x in imageCanvas.coords(bbox)])
			dataString += ", " + str(x) + ", " + str(y) + ", " + str(width) + ", " + str(height) + ", " + label + "\n"
			dataFile.write(dataString)
		dataFile.close()
		tkinter.messagebox.showinfo(title = "Export Successful", message = "Bounding Box data successfully written!")
		return
	# Functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Main Page Widgets - - - - - - - - - - - - - - - - - - - - - - - - -
	currentDirectory = os.getcwd()
	logo = Image.open(currentDirectory + "\\Images\\Logo.png")
	logo.thumbnail((210, 210))
	logo = ImageTk.PhotoImage(logo)
	classContainer = Frame(master)
	logoLabel = Button(classContainer, image = logo, command = exportBoundingBoxes)
	classLabel = Label(classContainer, text = "Classes", font = ("Facon", 31))
	classCanvas = Canvas(classContainer, highlightthickness = 0)
	classScrollbar = Scrollbar(classContainer, orient = "vertical", command = classCanvas.yview)
	classFrame = Frame(classCanvas)
	classCanvas.create_window((0, 0), window = classFrame, anchor= "nw")
	classCanvas.configure(yscrollcommand = classScrollbar.set)
	pixelSize = ImageTk.PhotoImage(Image.new("RGBA", (200, 50)))
	classButton = Button(classFrame, image = pixelSize, text = "Add New Class", command = createClassWidgets, compound = "c")
	
	masterCanvas = Canvas(master, highlightthickness = 0)
	imageCanvas = Canvas(masterCanvas, highlightthickness = 0)
	
	toolbarContainer = Frame(master)
	toolbarFrame = LabelFrame(toolbarContainer, text = "Toolbar")
	drag = ImageTk.PhotoImage(Image.open(currentDirectory + "\\Images\\DragIcon.png").resize((92, 92)))
	box = ImageTk.PhotoImage(Image.open(currentDirectory + "\\Images\\BoundingBoxIcon.png").resize((92, 92)))
	zoom = ImageTk.PhotoImage(Image.open(currentDirectory + "\\Images\\ZoomIcon.png").resize((92, 92)))
	resize = ImageTk.PhotoImage(Image.open(currentDirectory + "\\Images\\ResizeIcon.png").resize((92, 92)))
	zoomOut = ImageTk.PhotoImage(Image.open(currentDirectory + "\\Images\\ZoomOutIcon.png").resize((92, 92)))
	trash = ImageTk.PhotoImage(Image.open(currentDirectory + "\\Images\\TrashIcon.png").resize((92, 92)))
	backArr = ImageTk.PhotoImage(Image.open(currentDirectory + "\\Images\\BackArrow.png").resize((70, 70)))
	forwArr = ImageTk.PhotoImage(Image.open(currentDirectory + "\\Images\\ForwardArrow.png").resize((70, 70)))
	dragTool = Button(toolbarFrame, image = drag, command = dragState)
	boundingTool = Button(toolbarFrame, image = box, command = boundingState)
	zoomTool = Button(toolbarFrame, image = zoom, command = zoomState)
	resizeTool = Button(toolbarFrame, image = resize, command = resizeState)
	zoomOutTool = Button(toolbarFrame, image = zoomOut, command = zoomOutState)
	trashTool = Button(toolbarFrame, image = trash, command = trashState)
	backButton = Button(toolbarContainer, image = backArr, command = goBack)
	forwButton = Button(toolbarContainer, image = forwArr, command = goForward)
	# Main Page Widgets - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Form Application - - - - - - - - - - - - - - - - - - - - - - - - - -
	menuBar = Menu(master)
	fileMenu = Menu(menuBar, tearoff = 0)
	menuBar.add_cascade(label ='File', menu = fileMenu)
	fileMenu.add_command(label = "Create New Dataset", command = nameDirectory)
	fileMenu.add_command(label = "Open Dataset", command = openDataset)
	fileMenu.add_command(label ='Select Image Folder', command = selectFolder)
	fileMenu.add_command(label ='Save Dataset', command = saveDataset)
	
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
		zoomOutTool.grid(row = 2, column = 1, padx = 5, pady = 5)
		trashTool.grid(row = 1, column = 1, padx = 5, pady = 5)
		backButton.grid(row = 2, column = 0, pady = 5, sticky = "nw")
		forwButton.grid(row = 2, column = 0, pady = 5, sticky = "ne")
		
		master.update()
		classContainer.update()
		classCanvas.configure(width = classFrame.winfo_width(), height = master.winfo_height() - 300)
		classContainer.update()
		masterCanvas.configure(width = master.winfo_width() - (classContainer.winfo_width() * 2), height = classContainer.winfo_height())
		initialState = False
	
	classFrame.bind("<Configure>", lambda e: classCanvas.configure(scrollregion = classCanvas.bbox("all")))
	row, column = master.grid_size()
	master.rowconfigure(row, weight = 1)
	master.columnconfigure(column, weight = 1)
	# Form Application - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# Keyboard Shortcuts - - - - - - - - - - - - - - - - - - - - - - - - - -
	master.bind("<Control-s>", lambda event: saveDataset())
	master.bind("<Control-=>", lambda event: zoomCanvas(event))
	master.bind("<Control-minus>", lambda event: zoomOutImage(event))
	master.bind("<q>", lambda event: dragState())
	master.bind("<w>", lambda event: resizeState())
	master.bind("<e>", lambda event: boundingState())
	master.bind("<r>", lambda event: trashState())
	# Keyboard Shortcuts - - - - - - - - - - - - - - - - - - - - - - - - - -
	
	# mainloop, runs infinitely
	mainloop()