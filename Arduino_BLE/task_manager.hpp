#include "garden_task.hpp"
#include "BLE_task.hpp"

#ifndef TASK_MANAGER_HPP
#define TASK_MANAGER_HPP

class TaskManager {

public:
  BLETask task_1;       // every 5s
  GardenTask task_2;    // every 1min

  TaskManager() : task_1(5000), task_2(60000) {}

  void begin() {
    task_1.begin();
    task_2.begin();

    task_1.addService(task_2.getService());
  }

  void manage() {
    // BLE driver
    if (task_1.getState())
      task_1.run();

    if (task_1.connected()) {
      // Serial.println("JuPii");
      if (task_2.getState()) {
        task_2.run();
      }
    }
  }
};

#endif