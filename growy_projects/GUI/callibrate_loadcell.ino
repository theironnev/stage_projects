/*
 * https://circuits4you.com
 * 2016 November 25
 * Load Cell HX711 Module Interface with Arduino to measure weight in Kgs
 Arduino 
 pin 
 2 -> HX711 CLK
 3 -> DOUT
 5V -> VCC
 GND -> GND

 Most any pin on the Arduino Uno will be compatible with DOUT/CLK.
 The HX711 board can be powered from 2.7V to 5V so the Arduino 5V power should be fine.
*/

#include "HX711.h"  //You must have this library in your arduino library folder

#define DOUT_L  A4
#define CLK_L  A5

#define DOUT_R  3
#define CLK_R  2

//HX711 scale(DOUT, CLK);
HX711 scaleL;
HX711 scaleR;

//Change this calibration factor as per your load cell once it is found you many need to vary it in thousands
float cali_factor_left = 517080; //-106600 worked for my 40Kg max scale setup 
float cali_factor_right = 467850;
//=============================================================================================
//                         SETUP
//=============================================================================================
void setup() {
  Serial.begin(115200); 
  scaleL.begin(DOUT_L,CLK_L);
  scaleR.begin(DOUT_R,CLK_R);
  scaleL.set_scale(cali_factor_left);  //Calibration Factor obtained from first sketch
  scaleR.set_scale(cali_factor_right);
  scaleL.tare();             //Reset the scale to 0  
  scaleR.tare();
}

//=============================================================================================
//                         LOOP
//=============================================================================================
void loop() {

  if(Serial.available())
  {
    String temp = Serial.readStringUntil('\n');; //Serial.readStringUntil('\n')
        if(temp == "w" || temp == "W"){
         float weight = scaleL.get_units()+scaleR.get_units();
        Serial.println((1000*weight), 2);// waarde in gram met 2 decimaal 
    }
    if(temp == "t" || temp == "T" ){
      scaleL.tare();  //Reset the scale to zero    
      scaleR.tare();  
  }
    
    if(temp == 'c' || temp == 'C'){
      scaleL.set_scale();  //zero_factor
      scaleR.set_scale(); //zero_factorR
      scaleL.tare();             
      scaleR.tare();
      float left_mes = (1000*scaleL.get_units(10));  //Reset the scale to zero    
      float right_mes = (1000*scaleR.get_units(10))/500.0; 
      cali_factor_left = left_mes; 
      cali_factor_right = right_mes;
      Serial.println(left_mes);
      Serial.println(right_mes);
  }
}
}
//=============================================================================================
