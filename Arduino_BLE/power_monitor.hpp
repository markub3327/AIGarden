#ifndef POWER_MONITOR_HPP
#define POWER_MONITOR_HPP

class PowerMonitor {
  BLEFloatCharacteristic solarChar;
  BLEFloatCharacteristic reg12vChar;

  uint8_t pinSolar, pinReg12v;


  void writeValue(float solar, float reg12v) {
    solarChar.writeValue(solar);
    reg12vChar.writeValue(reg12v);
  }

public:
  PowerMonitor(const char* solarUuid,
              const char* reg12vUuid,
              uint8_t pinSolar, 
              uint8_t pinReg12v)
    : solarChar(solarUuid, BLERead | BLENotify),
      reg12vChar(reg12vUuid, BLERead | BLENotify),
      pinSolar(pinSolar),
      pinReg12v(pinReg12v)
  { }

  void begin() {
    // init value
    this->writeValue(0, 0);
  }

  void addCharacteristic(BLEService &service) {
    service.addCharacteristic(solarChar);
    service.addCharacteristic(reg12vChar);
  }

  void updateMonitor() {
    auto solar = (ADC_VREF * static_cast<float>(analogRead(pinSolar))) / (ADC_LEVELS * U_PRESCALER(27000, 6800));
    auto reg12v = (ADC_VREF * static_cast<float>(analogRead(pinReg12v))) / (ADC_LEVELS * U_PRESCALER(27000, 2700));
    this->writeValue(solar, reg12v);  // and update the battery level characteristic
  }
};

#endif