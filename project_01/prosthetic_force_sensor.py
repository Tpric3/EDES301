"""
--------------------------------------------------------------------------
Prosthetic Force Sensor
--------------------------------------------------------------------------
License:   
Copyright 2025 Tarik Price

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use the following hardware components to make a 6 finger augmentation: 
  - HT16K33 Display
  - Button
  - Red LED
  - Green LED
  - Potentiometer (analog input)
  - Servo

Requirements:
  - Hardware:
    - When Off:   Red LED is on; Green LED is off; Servo is returned to Grip level 0 with no line tension; Display is "OFF"
    - When Operational: Red LED is off; Green LED is on; Servo is "open"; Display is "ON: Grip Level"
    - Display number shows value of grip level (0~5, 0 = no grip ,5 = max grip)
    - Button
      - Any button press will turn off the device
    - Potentiometer
      - Potentiometer can be adjsted to change the "Grip Level"
    - User interaction:
      - Needs to be able to adjust the potentiometer to adjust the grip of the finger
      - User is able to see the level of grip and state of machine on the LCD
      - In any state, pressing button will disable the device and return the grip state to 0
      
      
# ------------------------------------------------------------------------
# Used Libraries
# ------------------------------------------------------------------------
import time

import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
from ht16k33 import HT16K33  # Assuming your display driver is named ht16k33.py
from servo import Servo  # Assuming the SG90 servo driver you posted

class finger_aug:
    def __init__(self):
        print("Program Start")

        # Hardware Setup
        self.adc_pin = "P1_19"
        self.button = "P2_2"
        self.red_led = "P2_4"
        self.green_led = "P2_6"
        self.servo_pin = "P1_36"

        # Initialize GPIOs
        GPIO.setup(self.button, GPIO.IN)
        GPIO.setup(self.red_led, GPIO.OUT)
        GPIO.setup(self.green_led, GPIO.OUT)

        # ADC and Servo
        ADC.setup()
        self.servo = Servo(self.servo_pin)
        self.display = HT16K33(bus=1, address=0x70)

        # Initial states
        self.display.set_colon(True)
        GPIO.output(self.green_led, GPIO.HIGH)
        GPIO.output(self.red_led, GPIO.LOW)

    def duty_cycle_calc(self, val):
        """Maps grip levels (0-8) to servo PWM duty cycle."""
        return 5 + (val / 8.0) * 5  # Maps to 5–10% duty

    def show_analog_value(self):
        """Reads potentiometer, displays grip level, and returns numeric level."""
        value = ADC.read_raw(self.adc_pin)
        grip_level = str(min(abs(int((value / 4095) * 8)), 8))
        display_string = "ON" + grip_level
        print(f"Raw Value: {value}, Grip Level: {grip_level}, Display: {display_string}")
        self.display.text(display_string)
        return int(grip_level)

    def run(self):
        is_on = True
        prev_button_state = 1

        try:
            while True:
                button_state = GPIO.input(self.button)

                # Button falling edge detection
                if prev_button_state == 1 and button_state == 0:
                    is_on = not is_on
                    time.sleep(0.2)  # Debounce

                    if not is_on:
                        print("Button pressed, turning OFF.")
                        PWM.set_duty_cycle(self.servo.pin, 7.5)  # Neutral
                        self.display.text("OFF")
                        GPIO.output(self.green_led, GPIO.LOW)
                        GPIO.output(self.red_led, GPIO.HIGH)
                    else:
                        print("Button pressed, turning ON.")
                        GPIO.output(self.red_led, GPIO.LOW)
                        GPIO.output(self.green_led, GPIO.HIGH)

                # If ON, show value and move servo
                if is_on:
                    grip_level = self.show_analog_value()
                    duty = self.duty_cycle_calc(grip_level)
                    PWM.set_duty_cycle(self.servo.pin, duty)

                prev_button_state = button_state
                time.sleep(0.1)

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        """Turn off everything safely."""
        print("Exiting and cleaning up...")
        PWM.stop(self.servo.pin)
        PWM.cleanup()
        GPIO.output(self.red_led, GPIO.LOW)
        GPIO.output(self.green_led, GPIO.LOW)
        self.display.text("----")
        self.display.set_colon(False)
        print("Program Complete")

# Run the program
if __name__ == "__main__":
    fin_aug = finger_aug()
    fin_aug.run()
