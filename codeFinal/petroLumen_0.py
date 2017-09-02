import sys
import pyglet
from pyglet.window import key
from pyglet.gl import *
from noise import pnoise1, snoise2
import random
import math
import csv
from ColorSender import *
from time import sleep

# OJO, ESTAS UTILIZANDO noise2D, LO QUE SIGNIFICA QUE ESTAS "DRAGGEANDO" EL CANVAS DE NOISE
# EN UNA DIRECCION DEFINIDA AL PRINCIPIO AL SETEAR timeXInc
# POR ESO EL RUIDO PARECE MOVERSE EN UNA DIRECCION.
# PARA EVITAR ESTO, USAR noise3d

#RGB values = 0 -> 100

window = pyglet.window.Window(visible=True, resizable=False, vsync=True)
#window.set_size(500,500)


#window.set_visible()

noArduino = False
enableDraw = True
showWire = False
showContrast = False

ledCount = 0
nodesX = []
nodesY = []
nodesValue = []
canvasWidth = 670
canvasHeight = 330
textos = []

timeX = random.random()
timeY = random.random()
timeXInc = (random.random() * 0.1) - 0.03
#timeYInc = (random.random() * 0.1) - 0.03
timeYInc = 0
# timeFarLimit = THE INCREMENT TO THE FAR LEFT/TOP OF SCREEN.
# NOISE VALUES FOR INTERMEDIATE NODES WILL BE INTERPOLATED FROM (time -> time + timeFarLimit)
timeFarLimit = 1

contrastStrength = 0.05 #OBSERVABLE strength VALUES: 0 -> 0.3
contrastStrengthMax = 0.3

# Serial Sender
colorSender = None

def load_data(archivo):
	global nodesX
	global nodesY
	global nodesValue
	
	global canvasWidth
	global canvasHeight
	
	global ledCount
	global textos
	
	with open(archivo,'r') as f:
		reader = csv.reader(f)
		
		for line in reader:
			if(line[0] == 'size'): # bounding Box de la instalacion real, en cm
				artworkWidth = int(line[1])
				artworkHeight = int(line[2])
				
				#canvasWidth = artworkWidth / float(artworkHeight) * 1000;
				#canvasHeight = artworkHeight / float(artworkWidth) * 1000;

				
				print "ArtWork Size: ", artworkWidth, artworkHeight
				print "Canvas Size: ", canvasWidth, canvasHeight
				continue
				
			rockX = (float(line[0]) / artworkWidth) * canvasWidth
			rockY = (float(line[1]) / artworkHeight) * canvasHeight
			nodesX.append(rockX)
			nodesY.append(rockY)
			nodesValue.append(255);
			
			textos.append(pyglet.text.Label(str(ledCount),x=int(rockX), y=int(rockY),font_name="Arial", font_size=10))
			
			ledCount += 1
			
		f.close()


def update(dt):
    global timeX
    global timeY
    global timeXInc
    global timeYInc
    

    timeX += timeXInc
    timeY += timeYInc


@window.event
def on_draw():
    #glLoadIdentity()
    window.clear()

    global nodesX
    global nodesY
    global nodesValue
    
    global timeFarLimit
    global canvasWidth
    global canvasHeight
    
    global colorSender
    
    global contrastStrength
    global showContrast

    for i in range(len(nodesX)):
        localTimeX = mapToRange(nodesX[i],0,canvasWidth,timeX, timeX + timeFarLimit)
        localTimeY = mapToRange(nodesY[i],0,canvasHeight,timeY, timeY + timeFarLimit)

        noiseValue = snoise2(localTimeX,localTimeY,octaves=1) # pnoise1(time,octaves)  range: -1 -> 1
        noiseValue = (noiseValue + 1) * 0.5 # range: 0 -> 1
        
        noiseValue = contrastSigmoid(noiseValue, contrastStrength) #OBSERVABLE strength VALUES: 0 -> 0.3
        
        vizScale = noiseValue * 30 # MAX CIRCLE SIZE
        nodesValue[i] = noiseValue * 100 # MAX COLOR VALUE TO SEND TO ARDUINO SYSTEM
        
        if enableDraw:
			# DRAW CIRCLES
			# SIZE VARIATION
			glColor4f(1,1,1,1)
			drawCircle(nodesX[i],nodesY[i],vizScale,20)
			
			# MAX SIZE
			glColor4f(0.2,0,0,1)
			drawCircle(nodesX[i],nodesY[i],30,20)
			
			# ROCK ID AND SIZE VALUE
			glColor4f(1,1,1,1)
			textos[i].text = str(i) + "  :  " + str("%.2f" % noiseValue)
			textos[i].draw();
	
	if enableDraw:
		drawDirectionArrow()
		if showWire:
			showConnectionPath()
		
		if showContrast:
			drawContrastCurve()
			#showContrast = False
		
	# SEND colors into ColorSender and out to Arduino
	if not noArduino:
		for i in range(len(nodesValue)):
			colorSender.setColor(i,0,0,nodesValue[i])
		colorSender.sendOut()
	
	
    '''
    # DRAW LITTLE SQUARE
    glColor4f(1,0,0,1.0)
    glBegin(GL_QUADS)

    glVertex2f(10,10)
    glVertex2f(20,10)
    glVertex2f(20,20)
    glVertex2f(10,20)

    glEnd()
    '''

    #glColor4f(1,1,1,1.0)
    #pyglet.text.Label(str(scale),x=100,y=100)

@window.event
def on_mouse_press(x,y,button,modifiers):
	global colorSender
	#print "MousePressing"
	
	'''
	if not noArduino:
		for i in range(len(nodesValue)):
			colorSender.setColor(i,0,0,nodesValue[i])
		
		#colorSender.resetLights()
		colorSender.sendOut()
	'''

@window.event
def on_mouse_drag(x,y,dx,dy,button,modifiers):
	global showContrast
	global contrastStrength
	global contrastStrengthMax
	global canvasWidth
	
	
	if showContrast:
		contrastStrength = mapToRange(x,0,canvasWidth,contrastStrengthMax,0)
	
	
	
@window.event
def on_key_press(symbol, modifiers):
	global colorSender

	if symbol ==  key.R:
		#print (" || GOING TO RESET LIGHTS")
		if not noArduino:
			colorSender.resetLights()
	
	if symbol ==  key.T:
		evaluateInput(raw_input(" || Parametro,Valor -->  "))

	
def drawCircle(x,y,radius, res=10):
    #res = 10
    #glColor4f(1,1,1,1);
    #glBegin(GL_POLYGON)
    glBegin(GL_LINES)
    for i in range(res):
        angle = ((math.pi * 2) / res) * i
        vX = x + (radius * math.cos(angle))
        vY = y + (radius * math.sin(angle))
        glVertex2f(vX,vY)
    glEnd()

def drawRectangle(x,y,w,h):
	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
    ('v2i', (x,y,x+w,y,x+w,y+h,x,y+h))
)
	'''
	glBegin(GL_QUADS)
	glVertex2f(x,y)
	glVertex2f(x + w,y)
	glVertex2f(x + w,y + h)
	glVertex2f(x,y + h)
	glEnd()
	'''

def mapToRange(value, sourceMin, sourceMax, targetMin, targetMax):
    # SPAN OF EACH RANGE
    sourceSpan = sourceMax - sourceMin
    targetSpan = targetMax - targetMin

    # NORMALIZE VALUE
    valueScaled = float(value - sourceMin) / float(sourceSpan)

    # TRANSPOLATE TO TARGETSPAN
    return targetMin + (valueScaled * targetSpan)

def contrastSigmoid(x, strength):
	y = 0;
	if x <= 0.5:
		y = (strength * x) / (strength + 0.5 - x)
	else:
		x2 = 1-x
		y = (strength * x2) / (strength + 0.5 - x2)
		y = 1-y
	return y
	
def drawDirectionArrow():
	
	
	glColor4f(1,0,0,1)
	
	glPushMatrix()
	glTranslatef(canvasWidth * 0.5, canvasHeight * 0.5,0)
	
	drawCircle(0,0,5,20)
		
	glBegin(GL_LINE_STRIP)
	glVertex2f(0,0)
	glVertex2f(-(timeXInc * 1000), -(timeYInc * 1000))

	glEnd()
	
	glPopMatrix()
	
def showConnectionPath():
	global ledCount
	global nodesX
	global nodesY
	
	glColor4f(0,1,0,1)
	glBegin(GL_LINE_STRIP)
	
	for i in range(ledCount):
		glVertex2f(nodesX[i], nodesY[i])
	
	glEnd()
	
def drawContrastCurve():
	global contrastStrength
	global canvasWidth
	
	res = 100
	unitSize = canvasWidth / res
	#print res, unitSize
	for i in range(res):
		colorValue = contrastSigmoid(i/float(res),contrastStrength) # 0 -> 0.3 OBSERVABLE strength VALUE
		glColor4f(colorValue,colorValue,colorValue,1)
		drawRectangle(i * unitSize, 0, unitSize, 50)
		#drawCircle(i * unitSize, 100, 20);
		

	
	
def evaluateInput(textInput):
	textInput = textInput.split(" ")
	print (textInput)
	
	if len(textInput) == 1:
		if textInput[0] == "stats":
			print "X Motion: ", -timeXInc, "\nY Motion: ", timeYInc, "\nLED count: ", ledCount
		elif textInput[0] == "reset":
			colorSender.resetLights()
		elif textInput[0] == "test":
			colorSender.testLights()
		elif textInput[0] == "wire":
			global showWire
			showWire = not showWire
		elif textInput[0] == "contrast":
			global showContrast
			showContrast = not showContrast
			
	elif len(textInput) == 2:
		if textInput[0] == "draw":
			global enableDraw
			enableDraw = bool(int(textInput[1]))
			#print enableDraw
		elif textInput[0] == "show":
			led = int(textInput[1])
			colorSender.turnOffLights()
			colorSender.setColor(led,100,100,100)
			colorSender.sendOut()
			sleep(2)
			

@window.event
def on_show():
    print " || APP START"

    global colorSender
    
    window.clear()
    #glClear(0)
    #pyglet.gl.glClearColor(0,0,0, 1)
    window.set_size(canvasWidth,canvasHeight)

    
    load_data("piedrasDatos.csv")
    print "LedCount: ", ledCount
    
    if not noArduino:
		colorSender = ColorSender(ledCount);
		#colorSender.resetLights()

@window.event
def on_activate():
    pyglet.gl.glClearColor(0,0,0, 1)
    #print " || WINDOW ACTIVATED"

pyglet.clock.schedule_interval(update, 1.0/30.0) # assign refresh rate to function-> schedule_interval(functionToSchedule, FPS)


if __name__== "__main__":
	#sys.argv[0] es el mismo nombre del archivo a ejecutar
	if len(sys.argv) > 1:
		canvasWidth = int(sys.argv[1])
		canvasHeight = int(sys.argv[2])
	print ("Canvas Width x Height:",canvasWidth,"x",canvasHeight) 
	
	pyglet.app.run()

    
