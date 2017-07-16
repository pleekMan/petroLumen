import pyglet
from pyglet.gl import *
from noise import pnoise1
import random

window = pyglet.window.Window(visible=True, resizable=False, vsync=True)
window.set_size(400,400)

'''
def on_resize(width, height):
	"""Setup 3D viewport"""
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(70, 1.0*width/height, 0.1, 1000.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
window.on_resize = on_resize
window.set_visible()
'''

#window.set_visible()


time = random.random()
timeInc = (random.random() * 0.03) + 0.005
x = 0

def update(dt):
    global time
    time += timeInc

@window.event
def on_show():
    window.clear()
    glLoadIdentity()
    #glClear(0)
    #pyglet.gl.glClearColor(0,0,0, 1)
    print "WINDOW SHOWN"

@window.event
def on_activate():
    pyglet.gl.glClearColor(0,0,0, 1)
    print "WINDOW ACTIVATED"

@window.event
def on_draw():
    global x

    window.clear()
    #glLoadIdentity()

    scale = pnoise1(time,octaves=1) # pnoise1(time,octaves)  range: -1 -> 1
    scale = (scale + 1) * 0.5 # range: 0 -> 1
    #print scale
    scale *= window.height
    y = scale;
    size = 2

    # DRAW LITTLE SQUARE
    glColor4f(1,0,0,1.0)
    glBegin(GL_QUADS)

    glVertex2f(x,y)
    glVertex2f(x + size,y)
    glVertex2f(x + size, y + size)
    glVertex2f(x,y + size)

    glEnd()

    # DRAW BLACK RECTANGLE TO CLEAR THE WAY
    glColor4f(0,0,0,1.0)
    glBegin(GL_QUADS)

    glVertex2f(x+size,0)
    glVertex2f(x + 30,0)
    glVertex2f(x + 30,window.height)
    glVertex2f(x+size,window.height)

    glEnd()

    #glColor4f(1,1,1,1.0)
    #pyglet.text.Label(str(scale),x=100,y=100)

    x+= 1
    if x>window.width:
        x = 0


pyglet.clock.schedule_interval(update, 1.0/30.0) # assign refresh rate to function-> schedule_interval(functionToSchedule, FPS)
pyglet.app.run()
