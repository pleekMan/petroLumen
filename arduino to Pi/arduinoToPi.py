import serial

serialComm = serial.Serial('/dev/ttyACM0',9600) # ARDUINO RECOGNIZED TRANSFER PORT

 while True:
    if(serialComm.inWaiting()):
        data = serialComm.readline()
        print data

        #serialComm.write('1')
        #time.sleep(3)
        #serialComm.close()
