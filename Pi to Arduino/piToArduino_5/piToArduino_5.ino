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

// OK, EL PROBLEMA ESTABA USANDO ARDUINO LEONARDO, Q ES UNA MIERDA Y
// CAUSABA ALGUN TIPO DE DESCONFIGURACION DE LOS PUERTOS EN LA RASPI

#include <PololuLedStrip.h>

PololuLedStrip<12> ledStrip;

#define LED_COUNT 2
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
    Serial.print("New Data = ");
    /*
    char data[3];
     Serial.readBytes(data,3);
     
     for(int i=0; i<3;i++){
     Serial.println(data[i]);
     }
     */
    char colorValue =  Serial.read();
    Serial.println(byte(colorValue));

    // VALUE CODE = ANY VALUE ABOVE 100 IS CONSIDERED A MESSAGE AND
    // NOT A COLOR. THEREFORE, THE COLOR INPUT RANGE IS 0 -> 100
    // CODES:
    // 101 -> RESET LIGHT & RGB COUNTERS
    // 102 -> TEST LIGHTS
    if(byte(colorValue) > 100){

      if(byte(colorValue) == 101){
        lightCounter = 0;
        rgbCounter = 0;

        for( int i = 0; i < LED_COUNT;  ++i ){
          lights[i].red = 0;
          lights[i].green = 0;
          lights[i].blue = 0;
        }

        Serial.println(" || RESETTING LIGHT COUNTERS");
        Serial.println(" || REMEMBER: THIS PROGRAM ACCEPTS COLOR VALUES 0 -> 100 THAT ARE REMAPPED To 0 -> 255");

      }
      ///
      if(byte(colorValue) == 102){
        Serial.println(" || TESTING LIGHTS");
      }
    }
    else{
      assignToRgbChannel(rgbCounter, colorValue);

      Serial.print("R: ");
      Serial.print(lights[lightCounter].red);
      Serial.print("\tG: ");
      Serial.print(lights[lightCounter].green);      
      Serial.print("\tB: ");
      Serial.println(lights[lightCounter].blue);
      Serial.println("--");
      Serial.print("LIGHT # ->\t");
      Serial.println(lightCounter);
      Serial.print("CHANNEL ->\t");
      Serial.println(rgbCounter);
      Serial.println("------");


      if(rgbCounter >= 3 ){
        rgbCounter = 0;
        lightCounter++;
      } 

      if(lightCounter >= LED_COUNT){
        //ledStrip.write(lights, LED_COUNT);
        delay(2);
        lightCounter = 0; 
      }
    }

    Serial.println("######################");
  }


}


void assignToRgbChannel(int channel, char colorValue){
  
  colorValue = map(colorValue,0,100,0,255); // SERIAL INPUT RANGE IS 0 -> 100
  
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

  rgbCounter++;

}






















