import serial
import struct

serialComm = serial.Serial('/dev/ttyACM0',9600)
# ttyACM1 -> ARDUINO RECOGNIZED PORT.
# IT MIGHT CHANGE. CHECK PORT ON ARDUINO IDE AND AT: ls -l /dev OR lsusb
# IT MIGHT BE BETTER TO RUN THIS LINES IN THE PYTHON SHELL DIRECTLY

colorInput = raw_input("Input R,G,B: ")
colorInput.split(',')
colorInput.write(bytes(bufferData))
for i in range(3):
    serieComm.write(bytes(colorInput[i]))


bufferData = []
bufferData.append('1') # SOLO FUNCA CON NUEROS DE UN DIGITO
bufferData.append('2')
bufferData.append('3')
serieComm.write(bufferData)

arduinoSerial.write(bytes('2','utf-8'))

# THIS FUCKING WORKED
serieComm.write(struct.pack('>BBB',45,50,255))

# WITH THIS ON ARDUINO
'''
 if(Serial.available() >= 3){
    //data = Serial.read() - '0'; // -> ASCII DE  '0' ES 48
    
    //byte data[3];
    //Serial.readBytes(data,3);
    
    int data[3];
    for(int i=0; i<3; i++){
      data[i] = Serial.read();
      //Serial.print("1: ");  
      Serial.println(data[i]);
    }
'''
