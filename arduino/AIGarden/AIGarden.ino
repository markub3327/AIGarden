#include <Wire.h>
#include <DHT.h>
#include <Adafruit_BMP085_U.h>
#include <LiquidCrystal_I2C.h>

#include "screen.hpp"

// Initialize DHT sensor
DHT dht(2, DHT22);
float humidity_0, temp_0, heat_index;
unsigned long DHT_lastTime = 0;

// Initialize BMP sensor
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);
float pressure_0, temp_1;

// Initialize LCD
LiquidCrystal_I2C lcd(0x27, 20, 4);
Screen screen(10000);

// Soil
int soil_0, soil_1;

// Serial
unsigned long Serial_lastTime = 0;


void scroll() {
  for (int positionCounter = 0; positionCounter < 20; positionCounter++) {
    lcd.setCursor(positionCounter, 0);
    lcd.print(' ');

    lcd.setCursor(positionCounter, 1);
    lcd.print(' ');

    lcd.setCursor(positionCounter, 2);
    lcd.print(' ');

    lcd.setCursor(positionCounter, 3);
    lcd.print(' ');

    delay(100);
  }
}

void screen0() {
  scroll();

  lcd.setCursor(0, 0);
  lcd.print(F("Temp 0: "));
  lcd.print(temp_0);
  lcd.print((char)0xDF);
  lcd.print('C');

  lcd.setCursor(0, 1);
  lcd.print(F("Temp 1: "));
  lcd.print(temp_1);
  lcd.print((char)0xDF);
  lcd.print('C');

  lcd.setCursor(0, 2);
  lcd.print(F("Heat index: "));
  lcd.print(heat_index);
  lcd.print((char)0xDF);
  lcd.print('C');

  lcd.setCursor(0, 3);
  lcd.print(F("--------------------"));
}

void screen1() {
  scroll();

  lcd.setCursor(0, 0);
  lcd.print(F("Humidity: "));
  lcd.print(humidity_0);
  lcd.print('%');

  lcd.setCursor(0, 1);
  lcd.print(F("--------------------"));

  lcd.setCursor(0, 2);
  lcd.print(F("Press 0: "));
  lcd.print(pressure_0);
  lcd.print(F("hPa"));

  lcd.setCursor(0, 3);
  lcd.print(F("--------------------"));
}

void screen2() {
  scroll();

  lcd.setCursor(0, 0);
  lcd.print(F("Soil 0: "));
  lcd.print(soil_0);

  lcd.setCursor(0, 1);
  lcd.print(F("--------------------"));

  lcd.setCursor(0, 2);
  lcd.print(F("Soil 1: "));
  lcd.print(soil_1);

  lcd.setCursor(0, 3);
  lcd.print(F("--------------------"));
}

void setup() {
  Serial.begin(9600);

  lcd.init();
  lcd.backlight();

  lcd.setCursor(6, 0);
  lcd.print(F("AIGarden"));
  lcd.setCursor(0, 3);
  lcd.print(F(" Bc. Martin Kubovcik"));

  dht.begin();

  /* Initialise the sensor */
  if(!bmp.begin())
  {
    lcd.setCursor(0, 0);
    lcd.print(F("Ooops, no BMP085 detected"));
    return;
  }

  // End of init
  delay(5000);
}

void loop() {
  unsigned long currentTime = millis();

  // Read DHT sensor - every 2s (slow sensor)
  if (currentTime - DHT_lastTime >= 2000) {
    // save the last time
    DHT_lastTime = currentTime;
    
    humidity_0 = dht.readHumidity();
    temp_0 = dht.readTemperature();
  }

  // Read BMP sensor
  bmp.getTemperature(&temp_1);
  bmp.getPressure(&pressure_0);
  pressure_0 /= 100.0f;   // convert to hPa

  // Read Soil sensors - get mini-batch statistics
  soil_0 = 0; soil_1 = 0;
  for (int i = 0; i < 128; i++)
  {
    soil_0 += analogRead(A0);
    soil_1 += analogRead(A1);
  }
  soil_0 /= 128.0; soil_1 /= 128.0;

  // Compute heat index in Celsius (isFahreheit = false)
  heat_index = dht.computeHeatIndex((temp_0+temp_1)/2.0, humidity_0, false);

  // Send to RPi - every 5s
  if (currentTime - Serial_lastTime >= 5000) {
    // save the last time
    Serial_lastTime = currentTime;

    Serial.print(temp_0);
    Serial.print(';');
    Serial.print(temp_1);
    Serial.print(';');
    Serial.print(heat_index);
    Serial.print(';');
    Serial.print(humidity_0);
    Serial.print(';');
    Serial.print(pressure_0);
    Serial.print(';');
    Serial.print(soil_0);
    Serial.print(';');
    Serial.println(soil_1);
  }

  // Show on screen
  if (screen.currentScreen == 0)
  {
    screen.run(screen0);
  }
  else if (screen.currentScreen == 1)
  {
    screen.run(screen1);
  }
  else if (screen.currentScreen == 2)
  {
    screen.run(screen2);
  } else {
    screen.currentScreen = 0;
  }
}
