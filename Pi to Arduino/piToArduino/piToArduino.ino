// ESTE PROGRAMA RECIBE Y LEE SOLAMENTE UN DIGITO (O SE QUEDA CON EL ULTIMO DE VARIOS),
// TRANSMITIDOS POR SERIAL.
// EL SENDER MANDA CHARS QUE SE ENCODEAN COMO ASCII
// EL Serial.read LEE EL CODIGO ASCII, NO EL VALOR DE CHAR QUE SE MANDO
// EN EN ASCII, '2' = 50, '0' = 48. SI HACEMOS '2' - '0' = 2 (EN ASCII)

int data;

void setup(){
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  data = 3;
}

void loop(){
  
  
  if(Serial.available()){
    data = Serial.read() - '0'; // -> ASCII DE  '0' ES 48
    Serial.println(data);
  }
  
  
  digitalWrite(13, HIGH);
  delay(data * 100);
  digitalWrite(13, LOW);
  delay(data * 100);
  
}

