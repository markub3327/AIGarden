#include <Arduino_HTS221.h>
#include <Arduino_LPS22HB.h>

#include "physics.hpp"

#ifndef METEO_SENSOR_HPP
#define METEO_SENSOR_HPP


class MeteoSensor {
  BLEFloatCharacteristic tempChar;
  BLEFloatCharacteristic humidityChar;
  BLEFloatCharacteristic pressureChar;
  BLEFloatCharacteristic altitudeChar;
  BLEUnsignedCharCharacteristic waterChar;

  uint8_t waterPinRead, waterPinControl;

  void writeValue(float temp, float humidity, float pressure, float altitude, float water) {
    tempChar.writeValue(temp);
    humidityChar.writeValue(humidity);
    pressureChar.writeValue(pressure);
    altitudeChar.writeValue(altitude);
    waterChar.writeValue(water);
  }

public:
  MeteoSensor(const char* tempUuid,
              const char* humUuid,
              const char* presUuid,
              const char* altUuid,
              const char* waterUuid,
              uint8_t waterPinRead,
              uint8_t waterPinControl)
    : tempChar(tempUuid, BLERead | BLENotify),
      humidityChar(humUuid, BLERead | BLENotify),
      pressureChar(presUuid, BLERead | BLENotify),
      altitudeChar(altUuid, BLERead | BLENotify),
      waterChar(waterUuid, BLERead | BLENotify),
      waterPinControl(waterPinControl),
      waterPinRead(waterPinRead)
  { }

  void begin() {
    if (!HTS.begin()) {
      Serial.println("Failed to initialize humidity temperature sensor!");
      while (1) ;
    }

    if (!BARO.begin()) {
      Serial.println("Failed to initialize pressure sensor!");
      while (1) ;
    }

    pinMode(this->waterPinControl, OUTPUT);
    digitalWrite(this->waterPinControl, HIGH);

    // set init value
    this->writeValue(0, 0, 0, 0, 0);
  }

  void addCharacteristic(BLEService &service) {
    service.addCharacteristic(tempChar);
    service.addCharacteristic(humidityChar);
    service.addCharacteristic(pressureChar);
    service.addCharacteristic(altitudeChar);
    service.addCharacteristic(waterChar);
  }

  void updateMeteo() {
    auto temp = HTS.readTemperature();
    auto humidity = HTS.readHumidity();
    auto pressure = BARO.readPressure() * 10.0f;
    auto altitude = 44330 * (1 - pow(pressure/1013.25, 1/5.255));
    auto waterLevel = map(analogRead(this->waterPinRead), 0, ADC_LEVELS, 0, 100);

    this->writeValue(temp, humidity, pressure, altitude, waterLevel);
  }
};

#endif