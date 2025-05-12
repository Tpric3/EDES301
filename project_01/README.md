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



## Software Build Instructions

1. Make sure the following Python libraries are installed on your PocketBeagle:
  - ```bash
  - sudo apt-get update
  - sudo apt-get install -y python3-pip
  - pip3 install adafruit-blinka
  - sudo apt-get install -y python3-adafruit-bbio i2c-tools
2. Clone or copy project files found in project_01 directory
  - prosthetic_force_sensor.py #Main project file
  - configure_pins.sh
  - force_sensitive_resistor.py
  - servo.py # Driver for SG90 Servo Motor
  - ht16k33.py # Driver for LCD
  - run
## Software Operation Instructions

1. OPTIONAL: Mount Device using Velcro Straps
  - Wrap palm with Velcro furthest from servo
  - Wrap wrist with Velcro closest to servo
2. Power On
  - Use command "python3 prosthetic_force_sensor.py" to run program
  - The system starts in ON state by default (Green LED lit)
  - Initial servo activation confirms startup
3. Grip Adjustment via FSR
  - Pressing on the FSR increase grip
  - LCD Display updates to: OnX where X represents a range of 0-8 grip level
4. Reading Feedback
  - Green LED: System On
  - RED LED: System Off
  - Display: either OnX (0<X<8) or OFF
5. Turn off system
  - Press button
  - Grip resets to 0
  - Servo returns to initial position
  - Red LED lights up
  - Display reads "OFF"

NOTE: For more information on the hardware setup and a proper demonstration of the project, visit [INSERT HERE]

I want to give a huge thanks to Dr. Erik Welsh for his guidance throughout the completion of this project as well as Paul Kim for his original project which inspired the creation of this one
Link to Paul Kim's Project: https://www.hackster.io/pkim7035/6-finger-augmentation-with-pocketbeagle-d0ea5d


