import time

class FSRReader:
    def __init__(self, adc_pin):
        self.adc_pin = adc_pin  # The pin where the FSR is connected

    def read_fsr_voltage(self):
        # This method should return the voltage reading from the FSR (use actual code for ADC)
        # Example: simulated voltage reading between 0 and 3.3V
        voltage = read_voltage(adc_pin)
        return voltage

    def read_fsr_resistance(self, voltage):
        # Assuming a fixed resistor R = 10k ohms (change this based on your circuit)
        fixed_resistor = 10000  # 10k ohms
        if voltage == 0:
            return None
        resistance = (3.3 - voltage) * fixed_resistor / voltage  # Voltage divider formula
        return resistance

    def calculate_force(self, resistance):
        # Force is calculated based on the FSR's resistance (this may need adjustment based on FSR datasheet)
        if resistance is None:
            return None
        force = (1 / resistance) * 1000  # Example force calculation; adjust for your sensor
        return force

    def show_fsr_value(self):
        voltage = self.read_fsr_voltage()
        
        # Debugging voltage: Check for unrealistic voltage values
        if voltage < 0 or voltage > 3.3:
            print(f"Error: Invalid voltage reading: {voltage:.2f} V")
            return None
        
        resistance = self.read_fsr_resistance(voltage)
        
        # Debugging resistance: Check for unrealistic resistance values
        if resistance is None or resistance < 1000 or resistance > 1000000:
            print(f"Error: Invalid resistance reading: {resistance:.0f} Ω")
            return None

        force = self.calculate_force(resistance)
        
        # Debugging force: Check for unrealistic force values
        if force is None or force < 0:
            print(f"Error: Invalid force reading: {force:.2f} N")
            return None
        
        # If all readings are valid, print the values
        grip_level = self.determine_grip_level(force)

        # Debug output with the results
        print(f"Voltage: {voltage:.2f} V | Resistance: {resistance:.0f} Ω | Force: {force:.2f} N | Grip Level: {grip_level}")
        
        return grip_level

    def determine_grip_level(self, force):
        # Map the force to a grip level, adjust this logic as needed
        if force < 0.05:
            return 0  # No grip
        elif force < 0.2:
            return 1  # Light grip
        elif force < 0.5:
            return 2  # Medium grip
        else:
            return 3  # Strong grip

    def run(self):
        print("Program Start")
        try:
            while True:
                grip_level = self.show_fsr_value()  # Get grip level from FSR sensor
                
                if grip_level is None:
                    print("Error: Invalid FSR reading.")
                
                time.sleep(0.1)  # Sleep for 100ms, adjust as needed
                
        except KeyboardInterrupt:
            print("\nExiting and cleaning up...")
        finally:
            print("Program Complete")

if __name__ == "__main__":
    fsr_reader = FSRReader(adc_pin="A4")  # Replace with your actual ADC pin
    fsr_reader.run()
