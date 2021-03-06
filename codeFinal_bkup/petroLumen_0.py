import pyglet
from pyglet.gl import *
from noise import pnoise1, snoise2
import random
import math
import csv

# OJO, ESTAS UTILIZANDO noise2D, LO QUE SIGNIFICA QUE ESTAS "DRAGGEANDO" EL CANVAS DE NOISE
# EN UNA DIRECCION DEFINIDA AL PRINCIPIO AL SETEAR timeXInc
# POR ESO EL RUIDO PARECE MOVERSE EN UNA DIRECCION.
# PARA EVITAR ESTO, USAR noise3d

window = pyglet.window.Window(visible=True, resizable=False, vsync=True)
#window.set_size(500,500)


#window.set_visible()
nodesX = []
nodesY = []
canvasWidth = 1000
canvasHeight = 500

timeX = random.random()
timeY = random.random()
timeXInc = (random.random() * 0.06) - 0.03
timeYInc = (random.random() * 0.06) - 0.03
# timeFarLimit = THE INCREMENT TO THE FAR LEFT/TOP OF SCREEN.
# NOISE VALUES FOR INTERMEDIATE NODES WILL BE INTERPOLATED FROM (time -> time + timeFarLimit)
timeFarLimit = 1

def load_data(archivo):
	global nodesX
	global nodesY
	
	global canvasWidth
	global canvasHeight
	
	with open('ppiedras.csv','r') as f:
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
    global timeFarLimit
    global canvasWidth
    global canvasHeight

    for i in range(len(nodesX)):
        localTimeX = mapToRange(nodesX[i],0,canvasWidth,timeX, timeX + timeFarLimit)
        localTimeY = mapToRange(nodesY[i],0,canvasHeight,timeY, timeY + timeFarLimit)

        scale = snoise2(localTimeX,localTimeY,octaves=1) # pnoise1(time,octaves)  range: -1 -> 1
        scale = (scale + 1) * 0.5 # range: 0 -> 1
        #print scale
        scale *= 10 # MAX CIRCLE SIZE

        # DRAW CIRCLE
        drawCircle(nodesX[i],nodesY[i],scale,50)

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


def drawCircle(x,y,radius, res=10):
    #res = 10
    glColor4f(1,1,1,1);
    glBegin(GL_POLYGON)
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

@window.event
def on_show():
    window.clear()
    glClear(0)
    pyglet.gl.glClearColor(0,0,0, 1)
    
    load_data('ppiedras.csv')
    window.set_size(canvasWidth,canvasHeight)
    
    print "APP START"


@window.event
def on_activate():
    pyglet.gl.glClearColor(0,0,0, 1)
    print "WINDOW ACTIVATED"

pyglet.clock.schedule_interval(update, 1.0/30.0) # assign refresh rate to function-> schedule_interval(functionToSchedule, FPS)
pyglet.app.run()



    
