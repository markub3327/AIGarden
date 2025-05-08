

struct Charger {
  BLECharCharacteristic chargeChar;
  BLECharCharacteristic faultChar;

  Charger(const char* chargeUuid, const char* faultUuid)
    : chargeChar(chargeUuid, BLERead | BLENotify),
      faultChar(faultUuid, BLERead | BLENotify)
  { }

  void addCharacteristic(BLEService &service) {
    service.addCharacteristic(chargeChar);
    service.addCharacteristic(faultChar);
  }

  void writeValue(char charge, char fault) {
    chargeChar.writeValue(charge);
    faultChar.writeValue(fault);
  }
};