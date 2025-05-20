#include <ArduinoBLE.h>
#include "task_manager.hpp"
#include "physics.hpp"

TaskManager task_manager;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);

  analogReadResolution(ADC_BITS);

  task_manager.begin();
}

void loop() {
  task_manager.manage();
}





