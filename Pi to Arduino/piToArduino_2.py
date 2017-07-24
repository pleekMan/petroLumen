import serial
import struct

ledCount = 2
serialComm = serial.Serial('/dev/ttyACM0',115200)

##################

def resetLights():
	print " || RESETTING LIGHTS"
	serialComm.write(struct.pack('>B',int(codes["reset"])))
	
def testLights():
	print " || TESTING LIGHTS"
	serialComm.write(struct.pack('>B',int(codes["test"])))	

codes = {"reset":101, "test":102}
codeFunctions = {"reset":resetLights, "test":testLights}

##############

while True:
	colorInput = raw_input("Input R,G,B: ")
	print colorInput
	splittedInput = colorInput.split(",")
	print splittedInput

	if len(splittedInput) <= 1:
		# INPUT IS A CODE
		try:
			codeFunctions[splittedInput[0]]()
		except:
			print " || CODE: ", splittedInput[0], " DOES NOT EXIST"
	else:
		# INPUT IS A COLOR NUMBER	
		intValue = [int(splittedInput[0]),int(splittedInput[1]),int(splittedInput[2])]
		print intValue

		for i in range(ledCount):
			serialComm.write(struct.pack('>BBB',intValue[0],intValue[1],intValue[2]))



