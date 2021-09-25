#include <Arduino.h>

class Screen {
  private:
    unsigned long lastTime = 0;
    unsigned long _interval = 10000;

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

  public:
    unsigned int currentScreen = 0;

    Screen(unsigned long interval)
    {
      this->_interval = interval;
    }
    void run(void (*show)()) {  
      unsigned long currentTime = millis();

      // show content
      show();

      // Go to next screen
      if (currentTime - lastTime >= this->_interval) {
        // save the last time
        lastTime = currentTime;

        // clear LCD
        scroll();

        this->currentScreen ++;
      }
    }
};