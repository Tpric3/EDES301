# Prosthetic Force Sensor Project

This project implements a programmable prosthetic finger device using a PocketBeagle and custom 3D-printed hardware. The device features force control via an analog input (FSR), visual feedback through a 7-segment HT16K33 display, and actuation with an SG90 servo motor.

## Hardware Components

- HT16K33 7-Segment Display
- Tactile Button
- Red LED
- Green LED
- Force-Sensitive Resistor (FSR)
- SG90 Servo Motor
- PocketBeagle
- 10kΩ Resistor (for voltage divider with FSR and button circuit)

## Requirements

### Hardware Behavior

- Off State:
  - Red LED: ON
  - Green LED: OFF
  - Servo: Returns to grip level 0 (fully relaxed)
  - Display: Shows "OFF"

- Operational State:
  - Red LED: OFF
  - Green LED: ON
  - Servo: Opens based on FSR grip level
  - Display: Shows "ON" and current grip level (0–8)

- Grip Level Display:
  - Grip level calculated from FSR sensor readings
  - Display shows level from 0 (no grip) to 8 (max grip)


### User Interaction

- Button:
  - Pressing the button toggles the device ON/OFF
  - Pressing while ON disables the servo and resets grip to 0

- Force Sensor (FSR):
  - Adjust grip strength by pressing harder on the FSR
  - Recalibrates to discrete levels: 0–8 based on filtered force

- Display & LEDs:
  - Green LED indicates operational state
  - Red LED indicates device is turned off
  - HT16K33 display shows grip level or OFF

---
