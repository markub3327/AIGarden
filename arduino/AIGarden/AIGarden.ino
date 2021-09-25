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
float soil_0, soil_1;

// Time
union {
    struct {
      int day, month, year, hour, minute, second;
    } time_s;
    int time_a[6];
} time;

// IP address
char IPAddr[20];

void scroll() {
  for (int positionCounter = 0; positionCounter < 40; positionCounter++) 
  {
    lcd.setCursor(positionCounter, 0);
    lcd.print(' ');
 
    lcd.setCursor(positionCounter, 1);
    lcd.print(' ');
    delay(20);
  }
}

void screen0() {
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
}

void screen1() {
  lcd.setCursor(0, 0);
  lcd.print(F("Humidity: "));
  lcd.print(humidity_0);
  lcd.print('%');

  lcd.setCursor(0, 1);
  lcd.print(F("Press 0: "));
  lcd.print(pressure_0);
  lcd.print(F("hPa"));
}

void screen2() {
  lcd.setCursor(0, 0);
  lcd.print(F("Soil 0: "));
  lcd.print(soil_0);

  lcd.setCursor(0, 1);
  lcd.print(F("Soil 1: "));
  lcd.print(soil_1);
}

void screen3() {
  lcd.setCursor(5, 0);
  lcd.print(time.time_s.day);
  lcd.print('.');
  lcd.print(time.time_s.month);
  lcd.print('.');
  lcd.print(time.time_s.year);

  lcd.setCursor(6, 1);
  lcd.print(time.time_s.hour);
  lcd.print('.');
  lcd.print(time.time_s.minute);
  lcd.print('.');
  lcd.print(time.time_s.second);

  lcd.setCursor(0, 2);
  lcd.print(F("IP: "));
  lcd.print(IPAddr);
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
  scroll();
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
  soil_0 = 0.0; soil_1 = 0.0;
  for (int i = 0; i < 128; i++)
  {
    soil_0 += analogRead(A0);
    soil_1 += analogRead(A1);
  }
  soil_0 /= 128.0f; soil_1 /= 128.0f;

  // Compute heat index in Celsius (isFahreheit = false)
  heat_index = dht.computeHeatIndex((temp_0+temp_1)/2.0, humidity_0, false);

  // Send to RPi
  Serial.print("$READ;");
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

  // Show on screen
  if (screen.currentScreen == 0)
  {
    screen.run(screen0, scroll);
  }
  else if (screen.currentScreen == 1)
  {
    screen.run(screen1, scroll);
  }
  else if (screen.currentScreen == 2)
  {
    screen.run(screen2, scroll);
  }
  else if (screen.currentScreen == 3)
  {
    screen.run(screen3, scroll);
  } else {
    screen.currentScreen = 0;
  }
}

void serialEvent() {
  static int i = 0;
  static char inputString[256];

  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == '\n') {
      char* substring = strtok(inputString, ";");
      
      // process the command
      if (strstr(substring, "$TIME") != NULL)
      {
        substring = strtok(0, ";");
        i = 0;
        while (substring != 0)
        {
          time.time_a[i++] = atoi(substring);
          // Go to next substring
          substring = strtok(0, ";");
        } 
      }
      else if (strstr(substring, "$IP") != NULL)
      {
        substring = strtok(0, ";");
        while (substring != 0)
        {
          // save IP
          memset(IPAddr, 0, sizeof(IPAddr));
          memcpy(IPAddr, substring, strlen(substring));
 
          // Go to next substring
          substring = strtok(0, ";");
        }        
      }
    
      // clear buffer
      memset(inputString, 0, sizeof(inputString));
      i = 0;
    } else {
      inputString[i++] = inChar;
    }
  }
}