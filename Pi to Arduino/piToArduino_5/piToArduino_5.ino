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
 
 // OK, EL PROBLEMA ERA ESTABA USANDO ARDUINO LEONARDO, Q ES UNA MIERDA Y
 // CAUSABA ALGUN TIPO DE DESCONFIGURACION DE LOS PUERTOS EN LA RASPI

#include <PololuLedStrip.h>

PololuLedStrip<12> ledStrip;

#define LED_COUNT 10
rgb_color lights[LED_COUNT];

int lightCounter = 0;
int rgbCounter = 0;

void setup(){
  pinMode(13, OUTPUT);
  Serial.begin(115200);
  //data = 3;
}

void loop(){


  if(Serial.available()){
    Serial.println("New Data");
    /*
    char data[3];
     Serial.readBytes(data,3);
     
     for(int i=0; i<3;i++){
     Serial.println(data[i]);
     }
     */

    assignToRgbChannel(rgbCounter);
    rgbCounter++;

    Serial.print("R ");
    Serial.println(lights[lightCounter].red);
    Serial.print("G ");
    Serial.println(lights[lightCounter].green);      
    Serial.print("B ");
    Serial.println(lights[lightCounter].blue);
    Serial.println("------");
    Serial.print("rgbCounter -> ");
    Serial.println(rgbCounter);
    Serial.print("lightCounter -> ");
    Serial.println(lightCounter);

    if(rgbCounter >= 3 ){
      rgbCounter = 0;
      lightCounter++;
    } 

    if(lightCounter >= LED_COUNT){
      delay(2);
      ledStrip.write(lights, LED_COUNT);

      lightCounter = 0; 
    }

    Serial.println("######################");
  }


}


void assignToRgbChannel(int channel){
  char colorValue =  Serial.read();

  switch(channel){
  case 0:
    lights[lightCounter].red = colorValue;
    break;
  case 1:
    lights[lightCounter].green = colorValue;
    break;
  case 2:
    lights[lightCounter].blue = colorValue;
    break;
  }
}
















