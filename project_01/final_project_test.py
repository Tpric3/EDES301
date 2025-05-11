import time
import math
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from ht16k33 import HT16K33
from servo import Servo

class finger_aug:
    def __init__(self):
        print("Program Start")

        # Hardware Setup
        self.adc_pin = "P1_27"  # FSR input pin
        self.button = "P2_2"
        self.red_led = "P2_4"
        self.green_led = "P2_6"
        self.servo_pin = "P1_36"

        # Constants
        self.R_FIXED = 10000.0  # 10kΩ resistor
        self.VCC = 3.3          # ADC reference voltage

        # Initialize GPIOs
        GPIO.setup(self.button, GPIO.IN)
        GPIO.setup(self.red_led, GPIO.OUT)
        GPIO.setup(self.green_led, GPIO.OUT)

        ADC.setup()
        self.servo = Servo(self.servo_pin)
        self.display = HT16K33(bus=1, address=0x70)

        self.display.set_colon(True)
        GPIO.output(self.green_led, GPIO.HIGH)
        GPIO.output(self.red_led, GPIO.LOW)

    def read_voltage(self):
        """Read ADC voltage from the FSR."""
        analog_value = ADC.read(self.adc_pin)
        return analog_value * self.VCC

    def compute_resistance(self, v_out):
        """Calculate FSR resistance from output voltage."""
        if v_out <= 0 or v_out >= self.VCC:
            return None
        return self.R_FIXED * (self.VCC - v_out) / v_out

    def estimate_force(self, resistance):
        """Estimate force (N) using FSR 402 approximation."""
        if resistance is None or resistance <= 0:
            return 0.0
        force_g = 100000 * math.pow(1.0 / resistance, 1.5)
        return force_g / 100.0  # Convert to Newtons

    def show_fsr_value(self):
        """Read force from FSR, convert to grip level, update display."""
        voltage = self.read_voltage()
        resistance = self.compute_resistance(voltage)
        force = self.estimate_force(resistance)
        grip_level = min(int(force * 2), 8)  # Map force to level 0–8

        if resistance is None:
            print(f"Voltage: {voltage:.2f} V | Resistance: -- | Force: -- N | Grip Level: {grip_level}")
            self.display.text("ERR")
        else:
            print(f"Voltage: {voltage:.2f} V | Resistance: {resistance:.0f} Ω | Force: {force:.2f} N | Grip Level: {grip_level}")
            self.display.text("ON" + str(grip_level))

        return grip_level

    def duty_cycle_calc(self, val):
        return 5 + (val / 8.0) * 5  # 5–10% duty cycle

    def run(self):
        is_on = True
        prev_button_state = 1

        try:
            while True:
                button_state = GPIO.input(self.button)

                if prev_button_state == 1 and button_state == 0:
                    is_on = not is_on
                    time.sleep(0.2)

                    if not is_on:
                        print("Button pressed, turning OFF.")
                        PWM.set_duty_cycle(self.servo.pin, 7.5)
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
                    PWM.set_duty_cycle(self.servo.pin, duty)

                prev_button_state = button_state
                time.sleep(0.1)

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        print("Exiting and cleaning up...")
        PWM.stop(self.servo.pin)
        PWM.cleanup()
        GPIO.output(self.red_led, GPIO.LOW)
        GPIO.output(self.green_led, GPIO.LOW)
        self.display.text("----")
        self.display.set_colon(False)
        print("Program Complete")

# Run
if __name__ == "__main__":
    fin_aug = finger_aug()
    fin_aug.run()

