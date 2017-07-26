import pyglet
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

window = pyglet.window.Window(visible=True, resizable=False, vsync=True)
#window.set_size(500,500)


#window.set_visible()

noArduino = True;

ledCount = 0
nodesX = []
nodesY = []
nodesValue = []
canvasWidth = 1000
canvasHeight = 500
textos = []

timeX = random.random()
timeY = random.random()
timeXInc = (random.random() * 0.06) - 0.03
timeYInc = (random.random() * 0.06) - 0.03
# timeFarLimit = THE INCREMENT TO THE FAR LEFT/TOP OF SCREEN.
# NOISE VALUES FOR INTERMEDIATE NODES WILL BE INTERPOLATED FROM (time -> time + timeFarLimit)
timeFarLimit = 1

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
	
	with open("ppiedras_15.csv",'r') as f:
		reader = csv.reader(f)
		
		for line in reader:
			if(line[0] == 'size'): # bounding Box de la instalacion real, en cm
				artworkWidth = int(line[1])
				artworkHeight = int(line[2])
				print "ArtWork Size: ", artworkWidth, artworkHeight
				print "Canvas Size: ", canvasWidth, canvasHeight
				continue
				
			rockX = (float(line[0]) / artworkWidth) * canvasWidth
			rockY = (float(line[1]) / artworkHeight) * canvasHeight
			nodesX.append(rockX)
			nodesY.append(rockY)
			nodesValue.append(255);
			
			textos.append(pyglet.text.Label(str(ledCount),x=int(rockX), y=int(rockY),font_name="Arial", font_size=12))
			
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

    for i in range(len(nodesX)):
        localTimeX = mapToRange(nodesX[i],0,canvasWidth,timeX, timeX + timeFarLimit)
        localTimeY = mapToRange(nodesY[i],0,canvasHeight,timeY, timeY + timeFarLimit)

        noiseValue = snoise2(localTimeX,localTimeY,octaves=1) # pnoise1(time,octaves)  range: -1 -> 1
        noiseValue = (noiseValue + 1) * 0.5 # range: 0 -> 1
        
        noiseValue = contrastSigmoid(noiseValue, 0.05) #OBSERVABLE VALUES: 0 -> 0.3
        
        vizScale = noiseValue * 50 # MAX CIRCLE SIZE
        nodesValue[i] = noiseValue * 100 # MAX COLOR VALUE TO SEND TO ARDUINO SYSTEM

        # DRAW CIRCLE
        drawCircle(nodesX[i],nodesY[i],vizScale,50)
        textos[i].text = str(i) + " : " + str("%.2f" % noiseValue)
        textos[i].draw();
	
	
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
	print "MousePressing"
	
	if not noArduino:
		for i in range(len(nodesValue)):
			colorSender.setColor(i,0,0,nodesValue[i])
		
		#colorSender.resetLights()
		colorSender.sendOut()

@window.event
def on_key_press(symbol, modifiers):
	global colorSender
	print symbol, ord("r")
	if not noArduino:
		if symbol == ord("r") or ord("R"):
			colorSender.resetLights()

	
def drawCircle(x,y,radius, res=10):
    #res = 10
    glColor4f(1,1,1,1);
    #glBegin(GL_POLYGON)
    glBegin(GL_LINES)
    for i in range(res):
        angle = ((math.pi * 2) / res) * i
        vX = x + (radius * math.cos(angle))
        vY = y + (radius * math.sin(angle))
        glVertex2f(vX,vY)
    glEnd()

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

@window.event
def on_show():
    
    global colorSender
    
    window.clear()
    #glClear(0)
    #pyglet.gl.glClearColor(0,0,0, 1)
    
    load_data('ppiedras.csv')
    
    if not noArduino:
		colorSender = ColorSender(ledCount);
		
    window.set_size(canvasWidth,canvasHeight)
    
    print " || APP START"


@window.event
def on_activate():
    pyglet.gl.glClearColor(0,0,0, 1)
    print " || WINDOW ACTIVATED"

pyglet.clock.schedule_interval(update, 1.0/30.0) # assign refresh rate to function-> schedule_interval(functionToSchedule, FPS)
pyglet.app.run()



    
