class ColorSender:
	
	#ledCount = 2
	#colors = []

	def __init__(self, _ledCount):
		
		self.colors = []
		self.ledCount = _ledCount
		print "LEDS: ", self.ledCount
		
		for i in range(self.ledCount * 3):
			self.colors.append(255)
		
		try:
			serialComm = serial.Serial('/dev/ttyACM0',115200)
			print " || INITIALIZING ARDUINO SERIAL COMM -> port: /dev/ttyACM0 | 115200 bps", 
		except:
			print " || NO ARDUINO DETECTED, PUNK..!!"
			
		self.sendOut()
	
	
	def resetLights(self):
		print " || RESETTING LIGHTS"
		serialComm.write(struct.pack('>B',int(codes["reset"])))
	
	def testLights(self):
		print " || TESTING LIGHTS"
		serialComm.write(struct.pack('>B',int(codes["test"])))
		
	def setColor(self, led=0, r=0,g=0,b=0):
		if led < self.ledCount:
			self.colors[(3*led)+0] = r
			self.colors[(3*led)+1] = g
			self.colors[(3*led)+2] = b
		
	def sendOut(self):
		#intValue = [int(splittedInput[0]),int(splittedInput[1]),int(splittedInput[2])]
		#print intValue
		print " || SENDING OUT.."
		for i in range(self.ledCount):
			print " || LED",str(i)+":", int(self.colors[(3*i)+0]), int(self.colors[(3*i)+1]), int(self.colors[(3*i)+2])
			#serialComm.write(struct.pack('>BBB',colors[0],colors[1],colors[2]))
			##serialComm.write(struct.pack('>BBB',int(colors[(3*i)+0]),int(colors[(3*i)+1]),int(colors[(3*i)+2])))

