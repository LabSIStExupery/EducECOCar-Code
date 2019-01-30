#include <LiquidCrystal.h>
#include <SoftwareSerial.h>
#include <TinyGPS.h>
TinyGPS gps;
SoftwareSerial ss(2, 3);
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {
  ss.begin(9600);
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("INIT");
}

void loop() {
  if(ss.available())
    { 
      while(ss.available()) 
        {
          if (gps.encode(ss.read())) {              
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Spd : ");
        lcd.print(gps.f_speed_kmph());
        lcd.print(" km/h");
      lcd.setCursor(0,1);
      lcd.print("Sat:");
        lcd.print(gps.satellites());
      
          }
    }
  }
} 
