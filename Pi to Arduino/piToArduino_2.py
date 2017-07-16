import serial
import struct

ledCount = 10
serialComm = serial.Serial('/dev/ttyACM0',115200)

colorInput = raw_input("Input R,G,B: ")
print colorInput
splittedInput = colorInput.split(",")
print splittedInput
intValue = [int(splittedInput[0]),int(splittedInput[1]),int(splittedInput[2])]
print intValue

for i in range(ledCount):
    serialComm.write(struct.pack('>BBB',intValue[0] * i,intValue[1],intValue[2]))




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
