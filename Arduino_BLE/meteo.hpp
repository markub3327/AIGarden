

struct MeteoSensor {
  BLEFloatCharacteristic tempChar;
  BLEFloatCharacteristic humidityChar;
  BLEFloatCharacteristic pressureChar;
  BLEFloatCharacteristic altitudeChar;

  MeteoSensor(const char* tempUuid,
              const char* humUuid,
              const char* presUuid,
              const char* altUuid)
    : tempChar(tempUuid, BLERead | BLENotify),
      humidityChar(humUuid, BLERead | BLENotify),
      pressureChar(presUuid, BLERead | BLENotify),
      altitudeChar(altUuid, BLERead | BLENotify)
  { }

  void addCharacteristic(BLEService &service) {
    service.addCharacteristic(tempChar);
    service.addCharacteristic(humidityChar);
    service.addCharacteristic(pressureChar);
    service.addCharacteristic(altitudeChar);
  }

  void writeValue(float temp, float humidity, float pressure, float altitude) {
    tempChar.writeValue(temp);
    humidityChar.writeValue(humidity);
    pressureChar.writeValue(pressure);
    altitudeChar.writeValue(altitude);
  }
};