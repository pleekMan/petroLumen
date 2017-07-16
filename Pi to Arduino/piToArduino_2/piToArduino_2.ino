// ESTE PROGRAMA RECIBE Y LEE SOLAMENTE UN DIGITO (O SE QUEDA CON EL ULTIMO DE VARIOS),
// TRANSMITIDOS POR SERIAL.
// EL SENDER MANDA CHARS QUE SE ENCODEAN COMO ASCII
// EL Serial.read LEE EL CODIGO ASCII, NO EL VALOR DE CHAR QUE SE MANDO
// EN EN ASCII, '2' = 50, '0' = 48. SI HACEMOS '2' - '0' = 2 (EN ASCII)

//byte data[];

void setup(){
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  //data = 3;
}

void loop(){
  
  
  if(Serial.available()){
    //data = Serial.read() - '0'; // -> ASCII DE  '0' ES 48
    
    //byte data[3];
    //Serial.readBytes(data,3);
    
    int data[3];
    for(int i=0; i<3; i++){
      data[i] = Serial.read();
      //Serial.print("1: ");  
      Serial.println(data[i]);
    }
    /*
    for(int i=0; i<3; i++){
      Serial.println(data[i]);
    }
    */
  }
  
  /*
  digitalWrite(13, HIGH);
  delay(data * 100);
  digitalWrite(13, LOW);
  delay(data * 100);
  */
}

