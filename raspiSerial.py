import serial

serialComm = serial.Serial('/dev/serial0',9600)

while True:
    data = raw_input("Input byte/data: ")
    serialComm.write('1')
    #time.sleep(3)
    #serialComm.close()
