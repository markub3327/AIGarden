#include <ArduinoBLE.h>
#include <Arduino_HTS221.h>
#include <Arduino_LPS22HB.h>

#include "pins.hpp"
#include "physics.hpp"
#include "charger.hpp"
#include "meteo.hpp"
#include "soil_moisure.hpp"
#include "water_sensor.hpp"

// Bluetooth® Low Energy Battery Service
BLEService gardenService("19B10000-F8F2-537E-4F6C-D104768A1215");

// Bluetooth® Low Energy Battery Level Characteristic
BLEFloatCharacteristic batteryVoltageChar("19B11A01-F8F2-537E-4F6C-D104768A1215", BLERead | BLENotify);
BLEFloatCharacteristic solarVoltageChar("19B11A02-F8F2-537E-4F6C-D104768A1215", BLERead | BLENotify);
SoilMoisureSensor soilMoisureChar[2] = {{A0, "19B11B01-F8F2-537E-4F6C-D104768A1215", BLERead | BLENotify}, {A1, "19B11B02-F8F2-537E-4F6C-D104768A1215", BLERead | BLENotify}};
MeteoSensor meteoChar("19B11C01-F8F2-537E-4F6C-D104768A1215", "19B11C02-F8F2-537E-4F6C-D104768A1215", "19B11C03-F8F2-537E-4F6C-D104768A1215", "19B11C04-F8F2-537E-4F6C-D104768A1215");
Charger chargerChar("19B11D01-F8F2-537E-4F6C-D104768A1215", "19B11D02-F8F2-537E-4F6C-D104768A1215");
WaterSensor waterSensorChar(A2, "19B11E01-F8F2-537E-4F6C-D104768A1215", BLERead | BLENotify);



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);

  analogReadResolution(ADC_BITS);

  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, HIGH);
  delay(2000);
  digitalWrite(PUMP_PIN, LOW);

  if (!HTS.begin()) {
    Serial.println("Failed to initialize humidity temperature sensor!");
  }

  if (!BARO.begin()) {
    Serial.println("Failed to initialize pressure sensor!");
  }

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1);
  }
  BLE.setLocalName("AIGarden");
  BLE.setAdvertisedService(gardenService); // add the service UUID
  gardenService.addCharacteristic(batteryVoltageChar); // add the battery level characteristic
  gardenService.addCharacteristic(solarVoltageChar); // add the battery level characteristic
  for (auto & it : soilMoisureChar) {
    gardenService.addCharacteristic(it.characteristic);
    it.characteristic.writeValue(0);
  }
  meteoChar.addCharacteristic(gardenService);
  chargerChar.addCharacteristic(gardenService);
  gardenService.addCharacteristic(waterSensorChar.characteristic);
  waterSensorChar.characteristic.writeValue(0);
  chargerChar.writeValue(0, 0);
  meteoChar.writeValue(0.0f, 0.0f, 0.0f, 0.0f);
  batteryVoltageChar.writeValue(0.0f);
  solarVoltageChar.writeValue(0.0f);
  BLE.addService(gardenService);
  
  // start advertising
  BLE.advertise();

  Serial.println("Bluetooth® device active, waiting for connections...");
}

void loop() {
  // wait for a Bluetooth® Low Energy central
  BLEDevice central = BLE.central();

  // if a central is connected to the peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's BT address:
    Serial.println(central.address());
    analogWrite(LED_BUILTIN, 80);

    while (central.connected()) {
      long currentMillis = millis();
      // if 1min have passed, check the battery level:
      if (currentMillis - previousMillis >= 60000) {
        previousMillis = currentMillis;
        updateBatteryVoltage();
        updateSolarVoltage();
        updateSoilMoisure();
        updateMeteo();
        updateCharger();
        updateWaterLevel();
      }
    }
    // when the central disconnects, turn off the LED:
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
    analogWrite(LED_BUILTIN, 0);
  }
}

void updateBatteryVoltage() {
  /* Read the current voltage level on the A0 analog input pin.
     This is used here to simulate the charge level of a battery.
  */
  auto batteryVoltage = (ADC_VREF * static_cast<float>(analogRead(A7))) / (ADC_LEVELS * U_PRESCALER(27000, 6800));
  batteryVoltageChar.writeValue(batteryVoltage);  // and update the battery level characteristic
}

void updateSolarVoltage() {
  /* Read the current voltage level on the A0 analog input pin.
     This is used here to simulate the charge level of a battery.
  */
  auto solarVoltage = (ADC_VREF * static_cast<float>(analogRead(A6))) / (ADC_LEVELS * U_PRESCALER(27000, 2700));
  solarVoltageChar.writeValue(solarVoltage);  // and update the battery level characteristic
}

void updateSoilMoisure() {
  /* Read the current voltage level on the A0 analog input pin.
     This is used here to simulate the charge level of a battery.
  */
  for (auto & it : soilMoisureChar) {
    auto soilMoisureLevel = 100 - map(analogRead(it.pin), 0, ADC_LEVELS, 0, 100);
    it.characteristic.writeValue(soilMoisureLevel);  // and update the battery level characteristic
    
    if (soilMoisureLevel < 42) {
      analogWrite(PUMP_PIN, 200);
    } else {
      analogWrite(PUMP_PIN, 0);
    }
  }
}

void updateWaterLevel() {
    auto waterLevel = map(analogRead(waterSensorChar.pin), 0, ADC_LEVELS, 0, 100);
    waterSensorChar.characteristic.writeValue(waterLevel);

    if (waterLevel > 10) {
      analogWrite(PUMP_PIN, 0);
    }
}

void updateMeteo() {
  float temp = HTS.readTemperature();
  float humidity = HTS.readHumidity();
  float pressure = BARO.readPressure() * 10.0f;
  float altitude = 44330 * (1 - pow(pressure/1013.25, 1/5.255));

  meteoChar.writeValue(temp, humidity, pressure, altitude);
}

void updateCharger() {
  auto charge = digitalRead(CHARGE_PIN) == LOW ? 1 : 0;
  auto fault = digitalRead(FAULT_PIN) == LOW ? 1 : 0;

  chargerChar.writeValue(charge, fault);
}