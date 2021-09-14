#include <Arduino.h>

class Screen {
  private:
    unsigned long lastTime = 0;
    unsigned long _interval = 10000;
  public:
    unsigned int currentScreen = 0;

    Screen(unsigned long interval)
    {
      this->_interval = interval;
    }
    void run(void (*show)()) {  
      unsigned long currentTime = millis();

      if (currentTime - lastTime >= this->_interval) {
        // save the last time
        lastTime = currentTime;

        // show content
        show();

        this->currentScreen ++;
      }
    }
};