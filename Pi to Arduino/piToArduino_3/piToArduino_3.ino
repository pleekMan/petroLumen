/*
SI EL PUERTO SERIE dev/ttyACM0 desaparece:
 1- Apretar boton RESET en arduino.
 Enseguida (mientras esta reseteandose (flashea e LED13)) correr en TERMINAL:
 sudo avrdude -patmega32u4 -cavr109 -P/dev/ttyACM0 -b57600
 Fijarse si la IDE de Arduino vuelve a mostrar el puerto dev/ttyACM0
 2- Subir un programa vacio (solo setup() y LOOP())
 3- Ahora se deberia poder subir bien cualquier programa
 ---- SI NO FUNCA, CAMBIAR LA ENTRADA USB DE LA RASPI A OTRA 
 ---- SI NADA FUNCIONA, REBOOTEAR LA RASPI
 */

#include <PololuLedStrip.h>

PololuLedStrip<12> ledStrip;

#define LED_COUNT 1
rgb_color lights[LED_COUNT];

int lightCounter = 0;

void setup(){
  pinMode(13, OUTPUT);
  Serial.begin(115200);
  //data = 3;
}

void loop(){


  if(Serial.available()){

    /*
    char data[3];
     Serial.readBytes(data,1);
     
     for(int i=0; i<3; i++){
     Serial.print("R ");
     Serial.println(data[0]);
     Serial.print("G ");
     Serial.println(data[0]);      
     Serial.print("B ");
     Serial.println(data[0]);
     }
     */


    //for(int i=0; i < LED_COUNT; i++){

    int data[3];
    for(int i=0; i<3; i++){
      data[i] = Serial.read();
      //data[i] = Serial.parseInt();
      Serial.print("Recieved: ");
      Serial.println(data[i]);
    }

    lights[i].red = data[0];
    lights[i].green = data[1];
    lights[i].blue = data[2];

    Serial.print("R ");
    Serial.println(lights[i].red);
    Serial.print("G ");
    Serial.println(lights[i].green);      
    Serial.print("B ");
    Serial.println(lights[i].blue);
    Serial.println("------");
    //}

    delay(2);
    ledStrip.write(lights, LED_COUNT);

    Serial.println("######################");
  }


  /*
  digitalWrite(13, HIGH);
   delay(data * 100);
   digitalWrite(13, LOW);
   delay(data * 100);
   */
}










