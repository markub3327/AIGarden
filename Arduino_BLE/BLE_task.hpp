#include "api/Common.h"
#include "task.hpp"

#ifndef BLE_TASK_HPP
#define BLE_TASK_HPP

class BLETask : public Task {
  BLEDevice central;
  bool isAdvertise;
  bool isConnected;

  void update() override {
    if (!isAdvertise) {
      // start advertising
      BLE.advertise();
      Serial.println("Bluetooth® device active, waiting for connections...");
      isAdvertise = true;
    } else if (!isConnected) {
      // wait for a Bluetooth® Low Energy central
      central = BLE.central();

      // if a central is connected to the peripheral:
      if (central) {
        Serial.print("Connected to central: ");
        // print the central's BT address:
        Serial.println(central.address());
        // turn on the LED to indicate the connection:
        analogWrite(LED_BUILTIN, 10);

        isConnected = true;
      } else {
        isConnected = false;
      }
    // isConnected && !central.connected()
    } else {
      if (!central.connected())
      {
          // when the central disconnects, turn off the LED:
          analogWrite(LED_BUILTIN, 0);
          Serial.print("Disconnected from central: ");
          Serial.println(central.address());
          isConnected = false;
      }
    }
  }

public:
  template<typename... Args>
  BLETask(Args&&... args) : Task(std::forward<Args>(args)...), isAdvertise(false), isConnected(false) {}

  void begin() {
    // begin initialization
    if (!BLE.begin()) {
      Serial.println("starting BLE failed!");
      while (1);
    }
    BLE.setDeviceName("AIGarden");
  }

  bool connected() const { return central.connected(); }

  void addService(BLEService & service) {
    BLE.setAdvertisedService(service);
    BLE.addService(service);
  }
};

#endif