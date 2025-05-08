

struct SoilMoisureSensor {
  BLEUnsignedCharCharacteristic characteristic;
  uint8_t pin;

  template<typename... Args>
  SoilMoisureSensor(uint8_t pin, Args&&... args) : characteristic(std::forward<Args>(args)...), pin(pin)
  {  }
};