// Libraries
#include "Adafruit_GFX.h"
#include "Adafruit_ILI9341.h"
#include "Adafruit_STMPE610.h"

//Vars
unsigned int state = 1;

//Inits
Adafruit_ILI9341 tft = Adafruit_ILI9341(10, 9);
Adafruit_STMPE610 touch = Adafruit_STMPE610(8);

void title(int state){
  tft.fillRect(0, 0, 240, 30, ILI9341_BLACK);
  tft.setCursor(3, 3);
  tft.setTextSize(3);
  if(state == 1){ tft.print("Vitesse moy."); }
  if(state == 2){ tft.print(""); }
  if(state == 3){ tft.print("Autonomie"); }
}

void echo(int pos, float inp){
  tft.setTextSize(5);
  if(pos >= 4){ return(false); }
  if(pos == 1){ tft.setCursor(3, 32); }
  if(pos == 2){ tft.setCursor(3, 195); }
  if(pos == 3){ tft.setCursor(3, 277); }
  tft.print(inp);
}

void setup() {
  tft.begin();
  touch.begin();
  tft.fillScreen(ILI9341_BLACK);
  tft.drawLine(0, 160, 240, 160, ILI9341_WHITE);
  tft.setCursor(3, 167);
  tft.setTextSize(3);
  tft.print("Distance(km)");
  tft.drawLine(0, 243, 240, 243, ILI9341_WHITE);
  tft.setCursor(3, 248);
  tft.setTextSize(3);
  tft.print("Vitesse(km/h)");
}

void loop() {
  if(touch.touched()) { state = state + 1; tft.fillRect(0, 31, 240, 31, ILI9341_GREEN); }
  if(state >= 4){ state = 1; }
  tft.fillRect(0, 31, 240, 31, ILI9341_BLACK);
//Debut Programme
  title(state);
  echo(1, 8.98);
  echo(2, 78.8);
  echo(3, 6.66);

//Fin Programme
  delay(500);
}
