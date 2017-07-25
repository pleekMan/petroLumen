class ColorSender:
	
	ledCount = 2
	colors = []

	def __init__(self):
		
		try:
			serialComm = serial.Serial('/dev/ttyACM0',115200)
			print " || INITIALIZING ARDUINO SERIAL COMM -> port: /dev/ttyACM0 | 115200 bps", 
		except:
			print "NO ARDUINO DETECTED, PUNK..!!"
	
	
	def resetLights():
		print " || RESETTING LIGHTS"
		serialComm.write(struct.pack('>B',int(codes["reset"])))
	
	def testLights():
		print " || TESTING LIGHTS"
		serialComm.write(struct.pack('>B',int(codes["test"])))
		
	def addColorToPack(r=0,g=0,b=0):
		colors.append(r)
		colors.append(g)
		colors.append(b)
		
	def sendOut():
		intValue = [int(splittedInput[0]),int(splittedInput[1]),int(splittedInput[2])]
		print intValue

		for i in range(ledCount):
			#serialComm.write(struct.pack('>BBB',colors[0],colors[1],colors[2]))
			serialComm.write(struct.pack('>BBB',colors[(3*i)+0],colors[(3*i)+1],colors[(3*i)+2]))

