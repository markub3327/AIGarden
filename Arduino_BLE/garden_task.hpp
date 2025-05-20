#include "meteo.hpp"
#include "soil_moisure.hpp"
#include "power_monitor.hpp"
#include "pump_control.hpp"

#include "task.hpp"
#include "pins.hpp"

#ifndef GARDEN_TASK_HPP
#define GARDEN_TASK_HPP

class GardenTask : public Task {
  BLEService service;

  PowerMonitor powerMonitorChar;
  SoilMoisureSensor soilMoisureChar[2] = {
    {SOIL_MOISURE_1_READ, SOIL_MOISURE_1_CONTROL, "19B11B01-F8F2-537E-4F6C-D104768A1215"},
    {SOIL_MOISURE_2_READ, SOIL_MOISURE_2_CONTROL, "19B11B02-F8F2-537E-4F6C-D104768A1215"}
  };
  MeteoSensor meteoChar;
  // Charger chargerChar("19B11D01-F8F2-537E-4F6C-D104768A1215", "19B11D02-F8F2-537E-4F6C-D104768A1215");
  PumpControl pumpControl;

  void update() override {
    this->powerMonitorChar.updateMonitor();
    this->meteoChar.updateMeteo();
    for (auto & it : this->soilMoisureChar) {
      it.updateSoilMoisure();
    }
  }

public:
  template<typename... Args>
  GardenTask(Args&&... args) : Task(std::forward<Args>(args)...),
    service("19B10000-F8F2-537E-4F6C-D104768A1215"),
    powerMonitorChar("19B11A01-F8F2-537E-4F6C-D104768A1215", "19B11A02-F8F2-537E-4F6C-D104768A1215", SOLAR_PIN, REG_12V_PIN),
    meteoChar("19B11C01-F8F2-537E-4F6C-D104768A1215", "19B11C02-F8F2-537E-4F6C-D104768A1215", "19B11C03-F8F2-537E-4F6C-D104768A1215", "19B11C04-F8F2-537E-4F6C-D104768A1215", "19B11E01-F8F2-537E-4F6C-D104768A1215", WATER_LEVEL_READ, WATER_LEVEL_CONTROL),
    pumpControl(PUMP_PIN)
  { }

  void begin() {
      powerMonitorChar.addCharacteristic(this->service);
      powerMonitorChar.begin();

      for (auto & it : this->soilMoisureChar) {
        it.addCharacteristic(this->service);
        it.begin();
      }

      meteoChar.addCharacteristic(this->service);
      meteoChar.begin();

      pumpControl.begin();
  }

  BLEService& getService() {
    return this->service;
  }
};

#endif