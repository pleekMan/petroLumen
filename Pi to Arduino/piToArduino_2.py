import serial
import struct

ledCount = 2
serialComm = serial.Serial('/dev/ttyACM0',115200)

while True:
	colorInput = raw_input("Input R,G,B: ")
	print colorInput
	splittedInput = colorInput.split(",")
	print splittedInput

	if splittedInput[0] == "r":
		serialComm.write(struct.pack('>B',int(101)))
	else:	
		intValue = [int(splittedInput[0]),int(splittedInput[1]),int(splittedInput[2])]
		print intValue

		for i in range(ledCount):
			serialComm.write(struct.pack('>BBB',intValue[0],intValue[1],intValue[2]))


