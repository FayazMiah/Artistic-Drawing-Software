import pygame
import sys
from sys import setrecursionlimit
import math
from threading import Thread as spawn
import os
import base64
import tkinter
from tkinter import filedialog



# INITIALISATIONS
display_x = 1280
display_y = 720
pygame.init()
screen = pygame.display.set_mode((display_x, display_y))
pygame.display.set_caption("Art program")
clock = pygame.time.Clock()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
setrecursionlimit(6000)

canvas_surf = pygame.Surface((955,485), pygame.SRCALPHA)
canvas_rect = canvas_surf.get_rect(topleft = (125,125))
canvas_surf.fill("white")
canvas_surf.convert_alpha()

colourWheel = pygame.image.load('colourWheel.png').convert_alpha()
colourWheel = pygame.transform.scale(colourWheel, ((80,80)))
colourWheelRect = colourWheel.get_rect(topleft = (985,625))

shadeGradient = pygame.image.load('gradient.jpg').convert_alpha()
shadeSliderSurface = pygame.transform.scale(shadeGradient, (15,75))
shadeSliderRect = shadeSliderSurface.get_rect(topleft = (950, 627))



# COLOURS
gray = 	(63,65,70,255)
darkGray = (54,57,62,255)
darkerGray = (38, 40, 43, 255)

# vars

layers = []
brushes = []

layerContainerSurfaceBG = pygame.Surface((175,400))
layerContainerSurfaceBG.fill(darkGray)
layerContainerRectBG = layerContainerSurfaceBG.get_rect(center = (95,400))

layerContainerSurface = pygame.Surface((165,390))
layerContainerSurface.fill(gray)
layerContainerRect = layerContainerSurface.get_rect(center = (95,400))

layerButtons = []
storedLayers = []



selectedTool = None
currentColour = (0,0,0,255)
eraserSize = 10

font = pygame.font.Font('freesansbold.ttf', 24)

class createLayer:

    def __init__(self):
        super().__init__()

        self.priority = len(layers) + 1
        self.hidden = False
        self.name = "Layer " + str(len(layers) + 1)
        self.surface = pygame.Surface((955,485), pygame.SRCALPHA)
        self.surface.fill((255,255,255,0))
        self.rectangle = self.surface.get_rect(topleft = (125,125))
        layers.append(self)

        global layerContainerSurface
        buttonSurface = pygame.Surface((155, 30))
        buttonSurface.fill(darkGray)
        buttonRect = buttonSurface.get_rect(center = (82, (len(layers) * 40)))

        imageSurface = pygame.Surface((26,26))
        imageRect = imageSurface.get_rect(topleft = (2,2))
        imageData = [imageSurface, imageRect]
        self.buttons = [buttonSurface, buttonRect, imageData]

        storedLayers.append([buttonSurface, buttonRect, self, imageData])


        


previousBrushPoint = None 


class createBrush:

    def __init__(self, thickness, shape):
        super().__init__()
        self.thickness = thickness
        self.shape = shape

    def drawBrush(self):
        '''global currentColour
        global currentLayer
        layerSurf = currentLayer.surface
        mouse = pygame.mouse
        location = mouse.get_pos()
        x = location[0] - 125
        y = location[1] - 125
        if self.shape == "circle":
            newSurface = pygame.draw.circle(layerSurf, currentColour, (x,y), self.thickness, 0) #(r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
        elif self.shape == "square":
            newSurface = pygame.Surface(self.thickness, self.thickness)
            newSurface.fill(currentColour)
            layerSurf.blit(newSurface, x,y)'''


        global currentColour
        global currentLayer
        global previousBrushPoint
        global currentLayer
        currentPoint = pygame.mouse.get_pos()
        x = currentPoint[0] - 125
        y = currentPoint[1] - 125
        if previousBrushPoint:
            line = pygame.draw.line(currentLayer.surface, currentColour, previousBrushPoint, (x,y), width=self.thickness)
        previousBrushPoint = (x,y)


currentBrush = createBrush(5, "circle")
currentLayer = createLayer()

# Layer Data

# Tools Data

toolButtons = []
toolButtonDebounce = False
layerButtonDebounce = False

toolsBarSurface = pygame.Surface((115,610))
toolsBarSurface.fill(gray)
toolsBarSurfaceBG = pygame.Surface((125,620))
toolsBarSurfaceBG.fill(darkGray)

toolsBarBGRect = toolsBarSurface.get_rect(topleft = (0,100))
toolsBarRect = toolsBarSurface.get_rect(topleft = (5,105))


hueShiftSurfaces = []
hueShiftInputButtons = []

hueShiftSurface = pygame.Surface((400,200))
hueShiftRect = hueShiftSurface.get_rect(center = (640,360))
hueShiftSurface.fill(gray)
hueShiftSurfaces.append([hueShiftSurface, hueShiftRect])

hueShiftSliderSurface = pygame.Surface((290,10))
hueShiftSliderRect = hueShiftSliderSurface.get_rect(center = (640,360))
hueShiftSliderSurface.fill(darkGray)
hueShiftSurfaces.append([hueShiftSliderSurface, hueShiftSliderRect])

hueShiftSliderHandleSurface = pygame.Surface((25,25))
hueShiftSliderHandleRect = hueShiftSliderHandleSurface.get_rect(center = (640,360))
hueShiftSliderHandleSurface.fill(darkerGray)
hueShiftSurfaces.append([hueShiftSliderHandleSurface, hueShiftSliderHandleRect])
hueShiftInputButtons.append([hueShiftSliderHandleSurface, hueShiftSliderHandleRect, "handle"])

hueShiftPercentSurface = pygame.Surface((80,40))
hueShiftPercentRect = hueShiftPercentSurface.get_rect(center = (640,310))
hueShiftPercentSurface.fill(darkGray)

huePercentTextSurface = pygame.Surface((80,40))
huePercentTextBoxRect = huePercentTextSurface.get_rect(topleft = (0,0))
huePercentText = font.render("0%", True, "white", None)
huePercentTextRect = huePercentText.get_rect(center = (35,20))
huePercentTextSurface.fill(darkGray)
huePercentTextSurface.blit(huePercentText, huePercentTextRect)
hueShiftPercentSurface.blit(huePercentTextSurface, huePercentTextBoxRect)
hueShiftSurfaces.append([hueShiftPercentSurface, hueShiftPercentRect])

hueShiftExecuteSurface = pygame.Surface((25,25))
hueShiftExecuteRect = hueShiftExecuteSurface.get_rect(center = (475,290))
hueShiftExecuteSurface.fill("green")
hueShiftSurfaces.append([hueShiftExecuteSurface, hueShiftExecuteRect])
hueShiftInputButtons.append([hueShiftExecuteSurface, hueShiftExecuteRect, "execute"])


colourButtons = ["red", "yellow", "green", "cyan", "blue", "magenta"]

for i in range (0,6,1):
    colourButtonSurface = pygame.Surface((25,25))
    colourButtonRect = colourButtonSurface.get_rect(center = (535 + (i * 40),410))
    colourButtonSurface.fill(colourButtons[i])
    hueShiftInputButtons.append([colourButtonSurface, colourButtonRect, colourButtons[i]])
    hueShiftSurfaces.append([colourButtonSurface, colourButtonRect])







topBarSurface = pygame.Surface((1080,115))
topBarSurface.fill(gray)
topBarSurfaceBG = pygame.Surface((1080,125))
topBarSurfaceBG.fill(darkGray)

topBarBGRect = topBarSurfaceBG.get_rect(topleft = (0,0))
topBarRect = topBarSurface.get_rect(topleft = (5,5))

menuButtonSurfaceBG = pygame.Surface((120,120))
menuButtonSurfaceBG.fill(darkGray)
menuButtonRectBG = menuButtonSurfaceBG.get_rect()

menuButtonSurface = pygame.Surface((115,115))
menuButtonSurface.fill(gray)
menuButtonRect = menuButtonSurface.get_rect()

textSurface = pygame.Surface((101,40))
textBoxRect = textSurface.get_rect(topleft = (0,0))
text = font.render("File", True, "white", None)
textRect = text.get_rect(center = (50,20))
textSurface.fill(darkGray)
textSurface.blit(text, textRect)

fileButtonSurface = pygame.Surface((101,40))
fileButtonSurface.fill(darkGray)
fileButtonRect = fileButtonSurface.get_rect(topleft = (7,12))
fileButtonSurface.blit(textSurface, textBoxRect)

toolsButtonSurface = pygame.Surface((101,40))
toolsButtonSurface.fill(darkGray)
toolsButtonRect = toolsButtonSurface.get_rect(topleft = (7,62))
text = font.render("Tools", True, "white", None)
textRect = text.get_rect(center = (50,20))
textSurface.fill(darkGray)
textSurface.blit(text, textRect)
toolsButtonSurface.blit(textSurface, textBoxRect)


fileButtons = []
toolsMenuButtons = []

importSurface = pygame.Surface((125,75))
importRect = importSurface.get_rect(midleft = (135,55))
importSurface.fill(darkGray)

textSurface = pygame.Surface((125,75))
textBoxRect = textSurface.get_rect(topleft = (0,0))
text = font.render("Import", True, "white", None)
textRect = text.get_rect(center = (62,37))
textSurface.fill(darkGray)
textSurface.blit(text, textRect)
importSurface.blit(textSurface, textBoxRect)
fileButtons.append((importSurface, importRect, "import"))


exportSurface = pygame.Surface((125,75))
exportRect = exportSurface.get_rect(midleft = (285,55))
exportSurface.fill(darkGray)

textSurface = pygame.Surface((125,75))
textBoxRect = textSurface.get_rect(topleft = (0,0))
text = font.render("Export", True, "white", None)
textRect = text.get_rect(center = (62,37))
textSurface.fill(darkGray)
textSurface.blit(text, textRect)
exportSurface.blit(textSurface, textBoxRect)
fileButtons.append((exportSurface, exportRect, "export"))


saveSurface = pygame.Surface((125,75))
saveRect = saveSurface.get_rect(midleft = (435,55))
saveSurface.fill(darkGray)

textSurface = pygame.Surface((125,75))
textBoxRect = textSurface.get_rect(topleft = (0,0))
text = font.render("Save", True, "white", None)
textRect = text.get_rect(center = (62,37))
textSurface.fill(darkGray)
textSurface.blit(text, textRect)
saveSurface.blit(textSurface, textBoxRect)
fileButtons.append((saveSurface, saveRect, "save"))




hueSurface = pygame.Surface((125,75))
hueRect = hueSurface.get_rect(midleft = (925,55))
hueSurface.fill(darkGray)

textSurface = pygame.Surface((125,75))
textBoxRect = textSurface.get_rect(topleft = (0,0))
text = font.render("Hue Shift", True, "white", None)
textRect = text.get_rect(center = (62,37))
textSurface.fill(darkGray)
textSurface.blit(text, textRect)
hueSurface.blit(textSurface, textBoxRect)
toolsMenuButtons.append((hueSurface, hueRect, "hueShift"))




brushButtonSurf = pygame.Surface((50,50))
brushButtonRect = brushButtonSurf.get_rect(center = (57,80))
brushButtonSurf.fill("green")
toolButtons.append([brushButtonSurf,brushButtonRect, "brush"])

eraserButtonSurf = pygame.Surface((50,50))
eraserButtonRect = eraserButtonSurf.get_rect(center = (57,150))
eraserButtonSurf.fill("yellow")
toolButtons.append([eraserButtonSurf,eraserButtonRect, "eraser"])

fillButtonSurf = pygame.Surface((50,50))
fillButtonRect = fillButtonSurf.get_rect(center = (57,220))
fillButtonSurf.fill("blue")
toolButtons.append([fillButtonSurf,fillButtonRect, "fill"])

colourPickerButtonSurf = pygame.Surface((50,50))
colourPickerButtonRect = colourPickerButtonSurf.get_rect(center = (57,290))
colourPickerButtonSurf.fill("red")
toolButtons.append([colourPickerButtonSurf,colourPickerButtonRect, "colourPicker"])

regionSelectionButtonSurf = pygame.Surface((50,50))
regionSelectionButtonRect = regionSelectionButtonSurf.get_rect(center = (57,360))
regionSelectionButtonSurf.fill("orange")
toolButtons.append([regionSelectionButtonSurf,regionSelectionButtonRect, "regionSelection"])






# Layer Properties Data

propertiesSurface = pygame.Surface((190,710))
propertiesSurface.fill(gray)
propertiesSurfaceBG = pygame.Surface((200,720))
propertiesSurfaceBG.fill(darkGray)

propertiesSurfaceBGRect = propertiesSurfaceBG.get_rect(topleft = (1080,0))
propertiesSurfaceRect = propertiesSurface.get_rect(topleft = (1085,5))

textSurface = pygame.Surface((142, 32))
textBoxRect = textSurface.get_rect(center = (71,16))
text = font.render("New Layer", True, "white", None)
textRect = text.get_rect()
textSurface.fill(darkGray)

newLayerSurface = pygame.Surface((150,40))
newLayerSurface.fill(darkerGray)
newLayerRect = newLayerSurface.get_rect(center = (95,675))
layerButtons.append([newLayerSurface, newLayerRect, "newLayer"])
textSurface.blit(text, textRect)
newLayerSurface.blit(textSurface, textBoxRect)



priorityUpSurface = pygame.Surface((150,20))
priorityUpSurface.fill("red")
priorityUpRect = priorityUpSurface.get_rect(center = (95,40))
layerButtons.append([priorityUpSurface, priorityUpRect, "priorityUp"])

priorityDownSurface = pygame.Surface((150,20))
priorityDownSurface.fill("orange")
priorityDownRect = priorityDownSurface.get_rect(center = (95,70))
layerButtons.append([priorityDownSurface, priorityDownRect, "priorityDown"])

duplicateLayerSurface = pygame.Surface((150,20))
duplicateLayerSurface.fill("yellow")
duplicateLayerRect = duplicateLayerSurface.get_rect(center = (95,100))
layerButtons.append([duplicateLayerSurface, duplicateLayerRect, "duplicateLayer"])

hideLayerSurface = pygame.Surface((150,20))
hideLayerSurface.fill("blue")
hideLayerRect = hideLayerSurface.get_rect(center = (95,130))
layerButtons.append([hideLayerSurface, hideLayerRect, "hideLayer"])

clearLayerSurface = pygame.Surface((150,20))
clearLayerSurface.fill("pink")
clearLayerRect = clearLayerSurface.get_rect(center = (95,160))
layerButtons.append([clearLayerSurface, clearLayerRect, "clearLayer"])

for i, button in enumerate(layerButtons):
    if not (button[2] == "newLayer"):
        layerPropertyfont = pygame.font.Font('freesansbold.ttf', 15)
        textSurface = pygame.Surface((150, 20))
        textSurface.fill(darkGray)
        text = layerPropertyfont.render(button[2], True, "white", None)
        textRect = text.get_rect(center = (75,10))
        textSurface.blit(text, textRect)
        rect = button[0].get_rect(topleft = (0,0))
        button[0].blit(textSurface, rect)










# Pallete Data

paletteBarSurface = pygame.Surface((955,100))
paletteBarSurface.fill(gray)
paletteBarSurfaceBG = pygame.Surface((960,110))
paletteBarSurfaceBG.fill(darkGray)

paletteBarBGRect = paletteBarSurface.get_rect(topleft = (120,610))
paletteBarRect = paletteBarSurface.get_rect(topleft = (125,615))

palleteSlots = []
for i in range (1,7,1):
    surfaceSlot = pygame.Surface((80,80))
    slotRect = surfaceSlot.get_rect(topleft = (30 + (120 * i),625))
    surfaceSlot.fill(darkGray)
    slotData = [surfaceSlot, slotRect, None, i]
    palleteSlots.append(slotData)
    if i == 1:
        selectedPaletteSlot = slotData




def drawPaletteBar():
    screen.blit(paletteBarSurfaceBG, paletteBarBGRect)
    screen.blit(paletteBarSurface, paletteBarRect)


def drawTools():
    screen.blit(toolsBarSurfaceBG, toolsBarBGRect)
    screen.blit(toolsBarSurface, toolsBarRect)

    for button in toolButtons:
        toolsBarSurface.blit(button[0],button[1])


def drawPropertiesMenu():
    propertiesSurface.blit(layerContainerSurfaceBG, layerContainerRectBG)
    propertiesSurface.blit(layerContainerSurface, layerContainerRect)

    for item in layerButtons:
        propertiesSurface.blit(item[0], item[1])

    screen.blit(propertiesSurfaceBG, propertiesSurfaceBGRect)
    screen.blit(propertiesSurface, propertiesSurfaceRect)


def erase():
    mouse = pygame.mouse
    pos = pygame.mouse.get_pos()
    x = pos[0] - 125
    y = pos[1] - 125
    for i in range (math.floor(-eraserSize / 2),math.floor(eraserSize/2),1):
        for j in range (math.floor(-eraserSize / 2),math.floor(eraserSize/2),1):
            currentLayer.surface.set_at((x + i, y + j), (255,0,255,0)) # erase colour value

regionOn = False
selectionPoints = pygame.Surface((955,485), pygame.SRCALPHA).convert_alpha()
selectionPoints.fill((255,255,255,0))
selectingRegion = False
previousSelectionPoint = None
firstSelectionPoint = None
lines = []

def toolButtonPress():
    global selectedTool
    global toolButtonDebounce

    mouse = pygame.mouse
    pos = mouse.get_pos()
    x = pos[0] - 5
    y = pos[1] - 105
    for button in toolButtons: #button is an array of: [layer surf, layer rect, toolname]
        if button[1].collidepoint((x,y)) and mouse.get_pressed()[0] and not toolButtonDebounce:
            toolButtonDebounce = True
            def debounceFunction():
                global selectedTool
                global toolButtonDebounce
                if button[2] == "brush":
                    if not (selectedTool == "brush"):
                        selectedTool = "brush"
                    else:
                        selectedTool = None
                elif button[2] == "eraser":
                    if not (selectedTool == "eraser"):
                        selectedTool = "eraser"
                    else:
                        selectedTool = None
                elif button[2] == "fill":
                    if not (selectedTool == "fill"):
                        selectedTool = "fill"
                    else:
                        selectedTool = None
                elif button[2] == "colourPicker":
                    if not (selectedTool == "colourPicker"):
                        selectedTool = "colourPicker"
                    else:
                        selectedTool = None
                elif button[2] == "regionSelection":

                    global lines
                    global firstSelectionPoint
                    global previousSelectionPoint
                    global selectingRegion
                    global regionOn
                    global selectionPoints
                    if not (selectedTool == "regionSelection"):
                        selectedTool = "regionSelection"
                    else:
                        print("asd")
                        selectingRegion = False
                        regionOn = False
                        selectionPoints = pygame.Surface((955,485), pygame.SRCALPHA)
                        selectionPoints.fill((255,255,255,0))
                        previousSelectionPoint = None
                        firstSelectionPoint = None
                        selectedTool = None
                pygame.time.delay(300)
                toolButtonDebounce = False
            t = spawn(target=debounceFunction)
            t.start()

fillRecursionData = []
positionsAltered = []

def draw3x3(pos, surface, colour, fillFactor):


    if not ((fillFactor % 2) == 0):
        lowerBound = - (math.ceil(fillFactor/2)) + 1
        upperBound = math.ceil(fillFactor/2)
    else:
        lowerBound = -(fillFactor / 2)
        upperBound = fillFactor / 2

    try:
        lowerBound = int(lowerBound)
        upperBound = int(upperBound)
        x = pos[0]
        y = pos[1]
        global positionsAltered
        for i in range (lowerBound,upperBound,1): #changes with fill factor (0,1,1)
            for j in range (lowerBound,upperBound,1): 
                positionsAltered.append((x + i,y + j))

        newSurface = pygame.Surface((fillFactor,fillFactor), pygame.SRCALPHA)
        newSurface.fill(colour)
        surface.blit(newSurface, (x,y))
    except:
        print("error")


def growFill(startPosition, targetColour, fillColour, surface, counter, fillFactor):
    
    x = startPosition[0]
    y = startPosition[1]

    global positionsAltered

    counter += 1

    draw3x3(startPosition,surface,fillColour, fillFactor)

    if x + fillFactor >= surface.get_width() or x - fillFactor <= 0:
        return
    elif y + fillFactor >= surface.get_height() or y - fillFactor <= 0:
        return

    if counter >= 750: 
        global fillRecursionData
        fillRecursionData.append(startPosition)
        return


    if surface.get_at((x + fillFactor, y)) == targetColour and (x + fillFactor, y) not in positionsAltered:
        growFill((x + fillFactor, y), targetColour, fillColour, surface, counter, fillFactor)
    elif not (surface.get_at((x + math.floor(fillFactor / 2), y)) == fillColour):
        draw3x3((x + math.floor(fillFactor / 2), y), surface, fillColour, fillFactor)
    
    if surface.get_at((x - fillFactor, y)) == targetColour and (x - fillFactor, y) not in positionsAltered:
        growFill((x - fillFactor, y), targetColour, fillColour, surface, counter, fillFactor)
    elif not (surface.get_at((x - math.floor(fillFactor / 2), y)) == fillColour):
        draw3x3((x - math.floor(fillFactor / 2), y), surface, fillColour, fillFactor)
     
    if surface.get_at((x, y + fillFactor)) == targetColour and (x, y + fillFactor) not in positionsAltered: #unchanged locations
       growFill((x, y + fillFactor), targetColour, fillColour, surface, counter, fillFactor)
    elif not (surface.get_at((x, y + math.floor(fillFactor / 2))) == fillColour): # on boundary of irregular shape drawn
        draw3x3((x, y + math.floor(fillFactor / 2)), surface, fillColour, fillFactor)

    if surface.get_at((x, y - fillFactor)) == targetColour and (x, y - fillFactor) not in positionsAltered:
        growFill((x, y - fillFactor), targetColour, fillColour, surface, counter, fillFactor)
    elif not (surface.get_at((x, y - math.floor(fillFactor / 2))) == fillColour):
        draw3x3((x, y - math.floor(fillFactor / 2)), surface, fillColour, fillFactor)

     
def fillTool(startPosition, targetColour, fillColour, surface, fillFactor):
    x = startPosition[0]
    y = startPosition[1]
    global positionsAltered
    #targetColour = currentLayer.surface.get_at((x,y))
    growFill((x,y), targetColour, fillColour, surface, 0, fillFactor)
    fillComplete = False
    cyclesComplete = 0
    while not fillComplete:

        for pos in fillRecursionData:
            growFill(pos, targetColour, fillColour, surface, 0, fillFactor)
            #layer.surface.set_at(pos, "red")
            fillRecursionData.remove(pos)
        if len(fillRecursionData) == 0:
            fillComplete = True
        cyclesComplete += 1
        if cyclesComplete >= 50:
            print("too large region")
            print(cyclesComplete)
            fillRecursionData.clear()
            fillComplete = True
    positionsAltered = []

def getLayerByPriority(priorityPassed):
    for i, layer in enumerate(layers):
        if layer.priority == priorityPassed:
            return layer
    return False

def alterPriority(direction):
    # set new priority
    # swap priorities
    # layer 1 is highest priority

    #new method : swap surface data

    global currentLayer

    if direction == "up" and currentLayer.priority == 1:
        return
    if direction == "down" and currentLayer.priority == len(layers):
        return

    if direction == "up":
        targetLayer = getLayerByPriority(currentLayer.priority - 1)
        targetLayerSurfaceData = targetLayer.surface.copy()
        currentLayerSurfaceData = currentLayer.surface.copy()
        targetLayer.surface = currentLayerSurfaceData
        currentLayer.surface = targetLayerSurfaceData
        currentLayer = targetLayer

    if direction == "down":
        targetLayer = getLayerByPriority(currentLayer.priority + 1)
        targetLayerSurfaceData = targetLayer.surface.copy()

        currentLayerSurfaceData = currentLayer.surface.copy()
        targetLayer.surface = currentLayerSurfaceData

        currentLayer.surface = targetLayerSurfaceData
        currentLayer = targetLayer

def clearLayer(layer):
    layer.surface.fill((255,255,255,0))



def layerButtonPress():
    global currentLayer
    global layerButtonDebounce
    mouse = pygame.mouse
    pos = mouse.get_pos()
    x = pos[0] - 1085
    y = pos[1] - 5
    for button in layerButtons: #button is an array of: [layer button surf, layer button rect, button name]
        if button[1].collidepoint((x,y)) and mouse.get_pressed()[0] and not layerButtonDebounce:
            layerButtonDebounce = True
            def debounceFunction():
                global currentLayer
                global layerButtonDebounce
                global mergeToggle

                if button[2] == "newLayer" and len(layers) < 9:
                    newLayer = createLayer()
                    currentLayer = newLayer
                elif button[2] == "priorityUp":
                    alterPriority("up")
                elif button[2] == "priorityDown":
                    alterPriority("down")
                elif button[2] == "duplicateLayer"  and len(layers) < 9:
                    newLayer = createLayer()
                    newLayer.surface = currentLayer.surface.copy()
                elif button[2] == "hideLayer":
                    if currentLayer.hidden:
                        currentLayer.hidden = False
                    else:
                        currentLayer.hidden = True
                elif button[2] == "clearLayer":
                    print("asd")
                    clearLayer(currentLayer)

                pygame.time.delay(500)
                layerButtonDebounce = False
            t = spawn(target=debounceFunction)
            t.start()

def switchLayer():
    global currentLayer
    global layerButtonDebounce
    mouse = pygame.mouse
    pos = mouse.get_pos()
    x = pos[0] - 1100
    y = pos[1] - 210
    for button in storedLayers:
        if button[1].collidepoint((x,y)) and mouse.get_pressed()[0] and not layerButtonDebounce:
            layerButtonDebounce = True
            def debounceFunction():
                global currentLayer
                global layerButtonDebounce

                currentLayer = button[2]
                pygame.time.delay(300)
                layerButtonDebounce = False
            t = spawn(target=debounceFunction)
            t.start()

def updateLayerPreviews():
    global storedLayers
    for layerData in storedLayers:
        layer = layerData[2]
        imageData = layerData[3]
        imageSurface = imageData[0]
        imageRect = imageData[1]
        actualSurface = layer.surface
        surfaceCopy = actualSurface.copy()
        surfaceCopy = pygame.transform.scale(surfaceCopy, (26,26))
        imageSurface.fill("white")
        imageSurface.blit(surfaceCopy, (0,0))
        layerData[0].blit(imageSurface,imageRect)
        layerContainerSurface.blit(layerData[0], layerData[1])

def darkenSelectedLayer():
    for item in storedLayers:

        textSurface = pygame.Surface((85, 25))

        if item[2] == currentLayer:
            item[0].fill(darkerGray)
            textSurface.fill(darkerGray)
        else:
            item[0].fill(darkGray)
            textSurface.fill(darkGray)

        textBoxRect = textSurface.get_rect(midleft = (45,15))
        text = font.render(item[2].name, True, "white", None)
        textRect = text.get_rect()
        textSurface.blit(text, textRect)
        item[0].blit(textSurface, textBoxRect)


def toolActivated():

    global selectionPoints
    global regionOn
    
    pos = pygame.mouse.get_pos()
    if regionOn:
        x = pos[0] - 125
        y = pos[1] - 125
        if x >= selectionPoints.get_width() or y >= selectionPoints.get_height() or x < 0 or y < 0:
            
            return False
        if not (selectionPoints.get_at((x,y)) == ((0,0,255,0))):
            
            return False
    if pygame.mouse.get_pressed()[0] and selectedTool and canvas_rect.collidepoint(pos):
        
        return True
    else:
        
        return False

def setColourFromColourWheel():
    global colourWheel
    global currentColour
    global shadeSliderSurface
    global shadeSliderRect

    screen.blit(colourWheel, colourWheelRect)

    x = pygame.mouse.get_pos()[0] - 985
    y = pygame.mouse.get_pos()[1] - 625
    if colourWheel.get_rect().collidepoint((x,y)):
        if pygame.mouse.get_pressed()[0] and colourWheel.get_at((x,y))[3] > 0:
            colour = colourWheel.get_at((x,y))
            selectedPaletteSlot[2] = colour
            selectedPaletteSlot[0].fill(colour)
            currentColour = colour


def manageShades():

    global colourWheel
    global shadeSliderSurface
    global shadeSliderRect
    global layerButtonDebounce
    screen.blit(shadeSliderSurface, shadeSliderRect)

    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    if shadeSliderRect.collidepoint((x,y)):
        if pygame.mouse.get_pressed()[0] and shadeSliderSurface.get_at((x - 950,y - 627))[3] > 0 and not layerButtonDebounce:          
            layerButtonDebounce = True
            def debounceFunction():
                global layerButtonDebounce
                global currentColour
                r = currentColour[0]
                g = currentColour[1]
                b = currentColour[2]
                shade = abs((y - 630) / 70)
            
                if shade < 0.5:
                    multiplier = (1-shade/0.5) * 100
                    r = r - (r/100 * multiplier)
                    g = g - (g/100 * multiplier)
                    b = b - (b/100 * multiplier)
                    if r > 255 or r < 0 or g > 255 or g < 0 or b > 255 or b < 0:
                        return
                    colour = (r,g,b)
                    selectedPaletteSlot[2] = colour
                    selectedPaletteSlot[0].fill(colour)
                    currentColour = colour
                elif shade > 0.5:
                    shade -= 0.5
                    r = ((255 - r) * shade) + r
                    g = ((255 - g) * shade) + g
                    b = ((255 - b) * shade) + b
                    if r > 255 or r < 0 or g > 255 or g < 0 or b > 255 or b < 0:
                        return
                    colour = (r,g,b)
                    selectedPaletteSlot[2] = colour
                    selectedPaletteSlot[0].fill(colour)
                    currentColour = colour     
                pygame.time.delay(300)
                layerButtonDebounce = False

            t = spawn(target=debounceFunction)
            t.start()
            

def managePalleteSlots():
    global currentColour
    global selectedPaletteSlot
    for item in palleteSlots: #surfaceSlot, slotRect, None, i
        surfaceSlot = item[0]
        slotRect = item[1]
        screen.blit(surfaceSlot, slotRect)
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        if slotRect.collidepoint((x,y)):
            if pygame.mouse.get_pressed()[0]:
                selectedPaletteSlot = item
                if item[2]:
                    currentColour = item[2]
                else:
                    item[2] = currentColour


def savePNG():

    try:
        name = "Save_1.png"
        num = 1
        nameFound = False
        while not nameFound:
                files = os.listdir()
                counter = len(files)
                for fileName in files:
                    if not (name == fileName):
                        counter -= 1
                if not (counter == 1):
                    nameFound = True
                else:
                    num += 1
                    name = "Save_" + str(num) + ".png"
        resultantSurface = pygame.Surface((955,485)).convert_alpha()
        resultantSurface.fill((255,255,255,0))
        for i in range (len(layers), 0,-1):
            layer = getLayerByPriority(i)
            if layer:
                resultantSurface.blit(layer.surface, layer.rectangle)
                    
        pygame.image.save(resultantSurface, name)
    except Exception as error:
        print("Error occured whilst saving to PNG: " + str(error))
        return False
    print("Successfully saved as : " + name)


def createSaveFile():
    try:
        name = "Save_1.txt"
        num = 1
        nameFound = False
        while not nameFound:
                files = os.listdir()
                counter = len(files)
                for fileName in files:
                    if not (name == fileName):
                        counter -= 1
                if not (counter == 1):
                    nameFound = True
                else:
                    num += 1
                    name = "Save_" + str(num) + ".txt"

            
                

        file = open(name, "x")
        file.close()


        '''for layer in layers:
            surface = layer.surface
            bytes = pygame.image.tobytes(layer.surface, "RGBA", False)
            saveFile.write("Layer " + str(layer.priority) + ": " + str(bytes))
            saveFile.close()'''

        with open(name, "wb") as f:
            for layer in layers:
                start = (layer.name + ":")
                x = eval(r"" + ("b'" + start + "'"))
                f.write(x) 
                bytesData = pygame.image.tobytes(layer.surface, "ARGB", False)
                print(len(bytesData))
                f.write(bytesData)
                f.write((f"\n").encode())

        f.close()
    except Exception as error:
        print("Error occured whilst saving to text document: " + error)
        return False
    print("Successfuly saved to text document as : " + name)


importingPNG = False
importPNGSurface = None
def importPNG():
    global importingPNG
    global importPNGSurface
    if not importSurface or not importPNGSurface:
        return
    mousePos = pygame.mouse.get_pos()
    x = mousePos[0]
    y = mousePos[1]
    screen.blit(importPNGSurface, (x - (importPNGSurface.get_width() / 2),y - (importPNGSurface.get_height() / 2)))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        currentLayer.surface.blit(importPNGSurface, (x - ((importPNGSurface.get_width() / 2) + 125),(y - (importPNGSurface.get_height() / 2) - 125)))
        importPNGSurface = None
        importingPNG = False

def decodeSaveFile():
    global currentLayer
    global importingPNG
    global importPNGSurface

    def openFile():
        filepath = filedialog.askopenfilename()
        return filepath


    filepath = openFile()
    isPNG = False
    
    if not filepath:
        return False, "File not chosen"

    if not filepath[-4:] == ".txt":

        if filepath[-4:] == ".png":
            isPNG = True
        else:
            return False, "Wrong file type"

    
    if not isPNG:
        file = open(filepath, "r")
        if not (str(file.read(8)) == "Layer 1:"):
            return False, "Wrong text format"
        file.close()

    if isPNG:
        image = pygame.image.load(filepath)
        if image.get_width() > 250 or image.get_height() > 250:
            if image.get_width() > image.get_height():
                scale = 250 / image.get_width()
            else:
                scale = 250 / image.get_height()
            image = pygame.transform.scale_by(image, scale)

        importPNGSurface = image
        importingPNG = True
        return True, None

    for layer in layers:
        clearLayer(layer)

    try:

        with open(filepath, 'rb') as f:

            lines = f.readlines()
            for i, line in enumerate(lines):
                layerName = line[0:8].decode() #"Layer 1: "
                image_bytes = line[9:]
                print("Layer " + str(i) + " Attempting to load in " + str(len(image_bytes)))

                priority = layerName[-2]
                layerFound = False
                layerSurface = pygame.image.frombytes(image_bytes, (955, 485), "RGBA", False).convert_alpha()
                for layer in layers:
                    if layer.priority == int(priority):
                        layer.surface = layerSurface
                        layerFound = True
            
                if not layerFound:
                    newlayer = createLayer()
                    newlayer.surface = layerSurface
    
    except Exception as error:
        return False, ("Something went wrong loading: " + str(error))
    return True, None

displayFilesMenu = False

def menuButtons():
    global fileButtonRect
    global layerButtonDebounce
    global toolsButtonRect
    mouse = pygame.mouse
    mousePos = mouse.get_pos()
    buttonRects = [fileButtonRect, toolsButtonRect]
    for i, buttonRect in enumerate(buttonRects):
        if buttonRect.collidepoint(mousePos):
            if mouse.get_pressed()[0] and not layerButtonDebounce:
                layerButtonDebounce = True

                def debounceFunction():
                    global layerButtonDebounce
                    global displayFilesMenu
                    if i == 0:
                        displayFilesMenu = True
                    elif i == 1:
                        displayFilesMenu = False
                    pygame.time.wait(300)
                    layerButtonDebounce = False

                t = spawn(target=debounceFunction)
                t.start()

shiftingHues = False

def menusManager():
    global displayFilesMenu
    global layerButtonDebounce
    mouse = pygame.mouse

    topBarSurface.fill(gray)
    topBarSurface.blit(menuButtonSurfaceBG, menuButtonRectBG)
    menuButtonSurface.blit(fileButtonSurface, fileButtonRect)
    menuButtonSurface.blit(toolsButtonSurface, toolsButtonRect)
    topBarSurface.blit(menuButtonSurface, menuButtonRect)

    if displayFilesMenu:
        topBarSurface.blit(importSurface, importRect)
        topBarSurface.blit(exportSurface, exportRect)
        topBarSurface.blit(saveSurface, saveRect)
    else:
        topBarSurface.blit(hueSurface, hueRect)
        
    screen.blit(topBarSurfaceBG, topBarBGRect)
    screen.blit(topBarSurface, topBarRect)
    if displayFilesMenu:
        for fileButton in fileButtons:
            if fileButton[1].collidepoint(pygame.mouse.get_pos()) and not layerButtonDebounce:
                if not pygame.mouse.get_pressed()[0]:
                    return
                layerButtonDebounce = True

                def debounceFunction():
                    global layerButtonDebounce

                    if fileButton[2] == "import":
                        success, error = decodeSaveFile()
                        if not success:
                            print(error)
                        else:
                            print("Successfully Loaded")
                    elif fileButton[2] == "export":
                        savePNG()
                    elif fileButton[2] == "save":
                        createSaveFile()

                    pygame.time.wait(300)
                    layerButtonDebounce = False

                t = spawn(target=debounceFunction)
                t.start()
    else:
        for button in toolsMenuButtons:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            if button[1].collidepoint((x,y)) and not layerButtonDebounce:
                if not pygame.mouse.get_pressed()[0]:
                    return
                layerButtonDebounce = True

                def debounceFunction():
                    global layerButtonDebounce
                    global shiftingHues

                    if button[2] == "hueShift":
                        if not shiftingHues:
                            shiftingHues = True
                        else:
                            shiftingHues = False

                    pygame.time.wait(300)
                    layerButtonDebounce = False

                t = spawn(target=debounceFunction)
                t.start()


pickingColour = False
def colourPickerFunction():

    global pickingColour
    global currentLayer
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    if pickingColour:
            pos = pygame.mouse.get_pos()
            return currentLayer.surface.get_at((x - 125,y - 125))
            pickingColour = False
    else:
        return False



hueShiftMultiplier = 0

def getNewValue(original, increase, multiplier):
    total = 255
    if multiplier == 0:
        return original
    if increase:
        return ((total - original) * (multiplier/100) + original)
    else:
        return (original - (original/100) * (multiplier))

currentColourShift = "red"

def shiftHueFunction(colour, shiftColour):
    global hueShiftMultiplier
    global shiftingHues
    if not shiftingHues:
        return
    red = colour[0]
    blue = colour[1]
    green = colour[2]
    patterns = {
        "red" : (1,-1,-1),
        "yellow" : (1,1,-1),
        "green" : (-1,1,-1),
        "cyan" : (-1,1,1),
        "blue" : (-1,-1,1),
        "magenta" : (1,-1,1)
    }
    scaleTypes = patterns[shiftColour]

    if scaleTypes[0] == -1:
        red = getNewValue(red, False, hueShiftMultiplier)
    else:
        red = getNewValue(red, True, hueShiftMultiplier)

    if scaleTypes[1] == -1:
        green = getNewValue(green, False, hueShiftMultiplier)
    else:
        green = getNewValue(green, True, hueShiftMultiplier)

    if scaleTypes[2] == -1:
        blue = getNewValue(blue, False, hueShiftMultiplier)
    else:
        blue = getNewValue(blue, True, hueShiftMultiplier)
    
    return (math.floor(red),math.floor(green),math.floor(blue))




def handleHueShift():
    global shiftingHues
    if not shiftingHues:
        return
    global hueShiftSliderHandleRect
    global hueShiftSliderHandleSurface
    global huePercentText
    global hueShiftMultiplier
    if not hueShiftSliderHandleRect.collidepoint(pygame.mouse.get_pos()) or not pygame.mouse.get_pressed()[0]:
        return
    x = (hueShiftSliderHandleRect.x)
    y = (hueShiftSliderHandleRect.y)
    newX = pygame.mouse.get_pos()[0]
    if newX > 770:
        newX = 770
    elif newX < 490:
        newX = 490
    hueShiftSliderHandleRect.x = newX - 15
    value = newX - 490
    percentage = math.floor((value / 280) * 100)
    huePercentText = font.render(str(percentage) + "%", True, "white", None)
    huePercentTextSurface.fill(darkGray)
    huePercentTextSurface.blit(huePercentText, huePercentTextRect)
    hueShiftPercentSurface.blit(huePercentTextSurface, huePercentTextBoxRect)
    hueShiftMultiplier = percentage

    
def checkHueShiftInput():
    mouse = pygame.mouse
    global layerButtonDebounce
    global currentLayer
    global shiftingHues
    if not shiftingHues:
        return
    for button in hueShiftInputButtons:
        if button[1].collidepoint(mouse.get_pos()) and not layerButtonDebounce and mouse.get_pressed()[0]:
            layerButtonDebounce = True

            def debounceFunction():
                global layerButtonDebounce
                global currentColourShift
                global hueShiftMultiplier

                if button[2] == "red":
                    currentColourShift = "red"
                elif button[2] == "yellow":
                    currentColourShift = "yellow"
                elif button[2] == "green":
                    currentColourShift = "green"
                elif button[2] == "cyan":
                    currentColourShift = "cyan"
                elif button[2] == "blue":
                    currentColourShift = "blue"
                elif button[2] == "magenta":
                    currentColourShift = "magenta" 
                elif button[2] == "execute":
                    for i in range (0, currentLayer.surface.get_width(), 1):
                        for j in range (0, currentLayer.surface.get_height(), 1):
                            if not hueShiftMultiplier == 0:
                                colour = currentLayer.surface.get_at((i,j))
                                alpha = colour[3]
                                newColour = shiftHueFunction(colour, currentColourShift)
                                r = newColour[0]
                                g = newColour[1]
                                b = newColour[2]
                                a = alpha
                                if r > 255:
                                    r = 255
                                if g > 255:
                                    g = 255
                                if b > 255:
                                    b = 255
                                if a > 255:
                                    a = 255
                                if r < 0:
                                    r = 0
                                if g < 0:
                                    g = 0
                                if b < 0:
                                    b = 0
                                if a < 0:
                                    a = 0

                                currentLayer.surface.set_at((i,j), (r,g,b,a))
                elif button[2] == "handle":
                    pass

                pygame.time.wait(300)
                layerButtonDebounce = False

            t = spawn(target=debounceFunction)
            t.start()



def getLineIntersection(line1, line2): # line is (p1,p2,gradient, midpoint (which is also used asy intercept))
    if (line1[2] - line2[2]) == 0:
        return
    x = ((line2[3][1] - line1[3][1])) / ((line1[2] - line2[2]))
    y = (line1[2] * x) + line1[3][1]
    return (x + (line1[3][0]),y)

def coordDistance(p1,p2):
    return math.sqrt(((p2[0] - p1[0]) * (p2[0] - p1[0]))  +  ((p2[1] - p1[1]) * (p2[1] - p1[1])))

def getAllLineIntersections():
    global lines
    points = []
    for lineX in lines:
        for lineY in lines:
            if not lineX == lineY:
                point = getLineIntersection(lineX, lineY)
                points.append(point)
    return points

def perpindicularFunction(p1,p2):
    dy = p2[1] - p1[1]
    dx = p2[0] - p1[0]
    if dy == 0 or dx == 0:
        return
    gradient = dy/dx
    perpindicular = -1 * (1/gradient)
    return perpindicular

def createCentralIntersecter(gradient, startPoint, endPoint):
    global selectionPoints
    length = 4000
    midpointX = (startPoint[0] + endPoint[0]) / 2
    midpointY = (startPoint[1] + endPoint[1]) / 2
    
    x1 = (midpointX + (length / 2))
    x2 = (midpointX - (length / 2))
    y1 = (x1 * gradient )
    y2 = (x2 * gradient)
    p1 = (x1 + midpointX,y1 + midpointY)
    p2 = (x2 + midpointX,y2 + midpointY)

    lines.append([p1,p2,gradient, (midpointX, midpointY)])
    
def getMeanPoint(points):
    totalX = 0
    totalY = 0
    counter = 0
    for point in points:
        if point:
            if point[0] and point[1]:
                if not point[0] < 0 and not point[1] < 0:
                    totalX += point[0]
                    totalY += point[1]
                    counter += 1
    if counter == 0:
        return
    avgX = (totalX / counter)
    avgY = (totalY / counter)
    return (avgX, avgY)

def createSelectionRegion():
    global selectingRegion
    if not selectingRegion:
        return
    global previousSelectionPoint
    global currentLayer
    global selectionPoints
    global firstSelectionPoint

    currentPoint = pygame.mouse.get_pos()
    x = currentPoint[0] - 125
    y = currentPoint[1] - 125

    if pygame.mouse.get_pressed()[0]:
        currentPoint = pygame.mouse.get_pos()
        if previousSelectionPoint:
            line = pygame.draw.line(selectionPoints, (255,0,0,0), previousSelectionPoint, (x,y), width=20)
            line = pygame.draw.line(selectionPoints, (255,0,0,128), previousSelectionPoint, (x,y), width=5)
            gradient = perpindicularFunction(previousSelectionPoint, (x,y))
            if gradient:
                createCentralIntersecter(gradient, previousSelectionPoint, (x,y))
        previousSelectionPoint = (x,y)
        if not firstSelectionPoint:
            firstSelectionPoint = (x,y)
    else:
        if not firstSelectionPoint:
            return

        line = pygame.draw.line(selectionPoints, (255,0,0,0), firstSelectionPoint, (x,y), width=10)
        line = pygame.draw.line(selectionPoints, (255,0,0,128), firstSelectionPoint, (x,y), width=3)
        previousSelectionPoint = None
        firstSelectionPoint = None
        selectingRegion = False
        #selectionPoints.fill((255,255,255,0))
        lines = []

def fillRegionArea(center):
    global selectionPoints
    global layerButtonDebounce
    if not layerButtonDebounce:
        layerButtonDebounce = True

        def debounceFunction():
            global layerButtonDebounce
            fillTool(center, (255,255,255,0), (0,0,255,0), selectionPoints, 5)
            layerButtonDebounce = False

        t = spawn(target=debounceFunction)
        t.start()



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
               pass
            if event.key == pygame.K_g:
                pass
    
    screen.blit(canvas_surf, canvas_rect)

    if importingPNG:
        importPNG()

    drawTools()
    drawPropertiesMenu()
    drawPaletteBar()

    toolButtonPress()
    layerButtonPress()
    switchLayer()
    updateLayerPreviews()
    darkenSelectedLayer()
    setColourFromColourWheel()
    managePalleteSlots()
    manageShades()
    menuButtons()
    menusManager()
    checkHueShiftInput()
    handleHueShift()
    createSelectionRegion()

    if not selectingRegion and len(lines) > 0:
        points = getAllLineIntersections()
        center = getMeanPoint(points)
        x = math.floor(center[0])
        y = math.floor(center[1])
        fillRegionArea((x,y))
        lines = []
        regionOn = True
    else:
        pass
    if toolActivated():

        if selectedTool == "brush":
            currentBrush.drawBrush()
        elif selectedTool == "eraser":
            erase()
        elif selectedTool == "fill":
            if not layerButtonDebounce:
                layerButtonDebounce = True

                def debounceFunction():
                    global layerButtonDebounce
                    pos = pygame.mouse.get_pos()
                    x = pos[0] - 125
                    y = pos[1] - 125
                    targetColour = currentLayer.surface.get_at((x,y))
                    fillTool((x,y), targetColour, currentColour, currentLayer.surface, 5)
                    layerButtonDebounce = False

                t = spawn(target=debounceFunction)
                t.start()
        elif selectedTool == "colourPicker":
            pickingColour = True
            colour = colourPickerFunction()
            currentColour = colour
            selectedPaletteSlot[0].fill(colour)
        elif selectedTool == "regionSelection":
            if not layerButtonDebounce:
                layerButtonDebounce = True

                def debounceFunction():
                    global layerButtonDebounce
                    global regionOn
                    global selectingRegion
                    global selectionPoints
                    global firstSelectionPoint
                    global previousSelectionPoint

                    if not selectingRegion:
                        selectingRegion = True
                        regionOn = True
                    else:
                        pass

                    pygame.time.wait(150)
                    
                    layerButtonDebounce = False

                t = spawn(target=debounceFunction)
                t.start()

    else:
        if selectedTool == "brush":
            previousBrushPoint = None

    for i in range (len(layers), 0,-1):
        layer = getLayerByPriority(i)
        if layer and not layer.hidden:
            screen.blit(layer.surface, layer.rectangle)

    if shiftingHues:
        for item in hueShiftSurfaces:
            screen.blit(item[0], item[1])

    screen.blit(selectionPoints, (125,125))

    pygame.display.update()
    clock.tick(160)
