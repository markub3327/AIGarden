#ifndef PUMP_CONTROL_HPP
#define PUMP_CONTROL_HPP

class PumpControl {
  uint8_t pin;

public:
  PumpControl(uint8_t pin) : pin(pin)
  { }

  void begin() {
    pinMode(this->pin, OUTPUT);

    analogWrite(this->pin, 100);
    delay(10000);
    analogWrite(this->pin, 0);
  }

  void setPump(int value) {
    analogWrite(this->pin, value);
  }
};

#endif