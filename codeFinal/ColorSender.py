import serial
import struct
from time import sleep

class ColorSender:
	
	#ledCount = 2
	#colors = []

	def __init__(self, _ledCount):
		
		self.colors = []
		self.ledCount = _ledCount
		print "LEDS: ", self.ledCount
		
		self.serialComm = None
		
		for i in range(self.ledCount * 3):
			self.colors.append(255)
		
		try:
			print " || INITIALIZING ARDUINO SERIAL COMM -> port: /dev/ttyACM0 | 115200 bps" 
			self.serialComm = serial.Serial('/dev/ttyACM0',115200)
		except:
			print " || NO ARDUINO DETECTED, PUNK..!!"
			
		self.resetLights()
	
	
	def resetLights(self):
		print " || RESETTING LIGHTS"
		self.serialComm.write(struct.pack('>B',int(101)))
		sleep(1)
	
	def testLights(self):
		print " || TESTING LIGHTS"
		#serialComm.write(struct.pack('>B',int(102)))
		for i in range(self.ledCount):
			self.turnOffLights()
			self.setColor(i,100,100,100)
			self.sendOut()
			sleep(0.5)
		
	def setColor(self, led=0, r=0,g=0,b=0):
		if led < self.ledCount:
			self.colors[(3*led)+0] = r
			self.colors[(3*led)+1] = g
			self.colors[(3*led)+2] = b
	
	def turnOffLights(self):
		for i in range(self.ledCount):
			self.setColor(led=i)
		
	def sendOut(self):
		#intValue = [int(splittedInput[0]),int(splittedInput[1]),int(splittedInput[2])]
		#print intValue
		#print " || SENDING OUT.."
		
		for i in range(self.ledCount):
			#print " || LED",str(i)+":", int(self.colors[(3*i)+0]), int(self.colors[(3*i)+1]), int(self.colors[(3*i)+2])
			self.serialComm.write(struct.pack('>BBB',int(self.colors[(3*i)+0]),int(self.colors[(3*i)+1]),int(self.colors[(3*i)+2])))
		self.serialComm.flush()
