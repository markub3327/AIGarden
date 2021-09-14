#!/bin/bash

# Compile project
arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old ./AIGarden

# Upload project to Arduino board
arduino-cli upload --port /dev/ttyUSB0 --fqbn arduino:avr:nano:cpu=atmega328old ./AIGarden
