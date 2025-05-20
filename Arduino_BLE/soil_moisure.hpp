#ifndef SOIL_MOISURE_HPP
#define SOIL_MOISURE_HPP

class SoilMoisureSensor {
  BLEUnsignedCharCharacteristic characteristic;
  uint8_t pinRead, pinControl;

public:
  template<typename... Args>
  SoilMoisureSensor(uint8_t pinRead, uint8_t pinControl, Args&&... args) : characteristic(std::forward<Args>(args)..., BLERead | BLENotify), pinRead(pinRead), pinControl(pinControl)
  {  }

  void begin() {
    pinMode(this->pinControl, OUTPUT);
    digitalWrite(this->pinControl, HIGH);

    // set init value
    this->characteristic.writeValue(0);
  }

  void updateSoilMoisure() {
    // Turn on sensor
    //analogWrite(this->pinControl, 127);
    //delay(10);   // debounce time

    // Read sensor
    auto soilMoisureLevel = 100 - map(analogRead(this->pinRead), 0, ADC_LEVELS, 0, 100);
    this->characteristic.writeValue(soilMoisureLevel);  // and update the battery level characteristic

    // Turn off sensor
    //analogWrite(this->pinControl, 0);
  }

  void addCharacteristic(BLEService &service) {
    service.addCharacteristic(characteristic);
  }
};

#endif