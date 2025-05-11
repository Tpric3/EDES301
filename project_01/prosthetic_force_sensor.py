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

Use the following hardware components to make a prosthetic finger controlled by a force sensitive resistor: 
  - HT16K33 Display
  - Button
  - Red LED
  - Green LED
  - FSR
  - Servo

Requirements:
  - Hardware:
    - When Off:   Red LED is on; Green LED is off; Servo is returned to Grip level 0 with no line tension; Display is "OFF"
    - When Operational: Red LED is off; Green LED is on; Servo is "open"; Display is "ON: Grip Level"
    - Display number shows value of grip level (0~8, 0 = no grip ,8 = max grip)
    - Button
      - Any button press will turn off the device
    - FSR
      - FSR can be pressed at varying magnitudes to change the "Grip Level"
    - User interaction:
      - Needs to be able to press finger down upon FSR to adjust the grip of the finger
      - User is able to see the level of grip and state of machine on the LCD
      - In any state, pressing button will disable the device and return the grip state to 0
      
"""      
      
# ------------------------------------------------------------------------
# Used Libraries
# ------------------------------------------------------------------------
import time
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from ht16k33 import HT16K33
from servo import Servo

class pros_finger:
    def __init__(self):
        print("Program Start")

        # Hardware pins
        self.adc_pin = "P1_27"      # FSR input
        self.button = "P2_2"        # Button input
        self.red_led = "P2_4"       # LED output
        self.green_led = "P2_6"     # LED output
        self.servo_pin = "P1_36"    # PWM output to servo

        # Constants
        self.VCC = 3.3              # ADC reference voltage

        # Setup
        GPIO.setup(self.button, GPIO.IN)
        GPIO.setup(self.red_led, GPIO.OUT)
        GPIO.setup(self.green_led, GPIO.OUT)
        ADC.setup()
        PWM.start(self.servo_pin, 7.5, 50)  # Neutral position

        self.display = HT16K33(bus=1, address=0x70)
        self.display.set_colon(True)

        GPIO.output(self.green_led, GPIO.HIGH)
        GPIO.output(self.red_led, GPIO.LOW)

        self.filtered_force = 0.0  # For smoothing FSR readings

    def read_voltage(self):
        """Read ADC voltage from the FSR."""
        analog_value = ADC.read(self.adc_pin)
        return analog_value * self.VCC

    def estimate_force(self, voltage):
        """Estimate force (N) from voltage using new calibration."""  # Plot voltage vs force to determine linear fit
        force = 16.46 * voltage - 1.475
        return max(force, 0.0)

    def show_fsr_value(self):
        """Read force from FSR, assign grip level by force thresholds, update display."""
        voltage = self.read_voltage()
        force = self.estimate_force(voltage)

        # Apply low-pass filter for smoothing
        self.filtered_force = 0.8 * self.filtered_force + 0.2 * force

        # Define grip level thresholds (N)
        thresholds = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

        # Assign grip level based on filtered force
        grip_level = 0
        for i, threshold in enumerate(thresholds):
            if self.filtered_force >= threshold:
                grip_level = i + 1

        grip_level = min(grip_level, 8)

        print(f"Voltage: {voltage:.2f} V | Force: {self.filtered_force:.2f} N | Grip Level: {grip_level}")
        self.display.text("ON" + str(grip_level))

        return grip_level


    def duty_cycle_calc(self, val):
        """Map grip level (0–8) to servo PWM duty cycle (5% to 10%)."""
        return 5 + (val / 8.0) * 5

    def run(self):
        is_on = True
        prev_button_state = GPIO.input(self.button)

        try:
            while True:
                button_state = GPIO.input(self.button)

                # Button debounce (check again after short delay)
                if prev_button_state == 1 and button_state == 0:
                    time.sleep(0.05)
                    if GPIO.input(self.button) == 0:
                        is_on = not is_on

                        if not is_on:
                            print("Button pressed, turning OFF.")
                            PWM.set_duty_cycle(self.servo_pin, 7.5)  # Neutral
                            self.display.text("OFF")
                            GPIO.output(self.green_led, GPIO.LOW)
                            GPIO.output(self.red_led, GPIO.HIGH)
                        else:
                            print("Button pressed, turning ON.")
                            GPIO.output(self.red_led, GPIO.LOW)
                            GPIO.output(self.green_led, GPIO.HIGH)

                if is_on:
                    grip_level = self.show_fsr_value()
                    duty = self.duty_cycle_calc(grip_level)
                    PWM.set_duty_cycle(self.servo_pin, duty)

                prev_button_state = button_state
                time.sleep(0.1)

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        print("Exiting and cleaning up...")
        PWM.stop(self.servo_pin)
        PWM.cleanup()
        GPIO.output(self.red_led, GPIO.LOW)
        GPIO.output(self.green_led, GPIO.LOW)
        self.display.text("----")
        self.display.set_colon(False)
        print("Program Complete")

# Run
if __name__ == "__main__":
    pros_fin = pros_finger()
    pros_fin.run()
