"""
--------------------------------------------------------------------------
Force Sensitive Resistor Driver
--------------------------------------------------------------------------
License:   
Copyright 2021-2025 - Tarik Price

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

Force Sensitive Resistor Driver

  

"""

import Adafruit_BBIO.ADC as ADC
import time
import math

# Setup
ADC.setup()
FSR_PIN = "P1_27"  # Change to your actual ADC input pin
R_FIXED = 10000.0  # 10kΩ resistor in voltage divider
VCC = 3.3          # PocketBeagle analog reference voltage

def read_voltage(pin):
    """Read ADC value and convert to actual voltage."""
    analog_value = ADC.read(pin)
    return analog_value * VCC

def compute_resistance(v_out):
    """Calculate FSR resistance from output voltage."""
    if v_out <= 0 or v_out >= VCC:
        return None  # Avoid divide by zero or invalid values
    return R_FIXED * (VCC - v_out) / v_out

def estimate_force(resistance):
    """Estimate force in Newtons based on empirical curve for FSR 402."""
    if resistance is None or resistance <= 0:
        return 0.0

    # Empirical curve approximation: log-log linear fit
    # For FSR 402: force (g) ≈ 100000 * (1/R)^1.5  [where R in ohms]
    # We'll return force in Newtons: 1 N ≈ 100 g
    force_g = 100000 * math.pow(1.0 / resistance, 1.5)
    force_n = force_g / 100.0
    return force_n

# Main loop
try:
    while True:
        voltage = read_voltage(FSR_PIN)
        resistance = compute_resistance(voltage)
        force = estimate_force(resistance)

        if resistance is None:
            print(f"Voltage: {voltage:.2f} V | Resistance: -- | Estimated Force: --")
        else:
            print(f"Voltage: {voltage:.2f} V | Resistance: {resistance:.0f} Ω | Estimated Force: {force:.2f} N")
        
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Stopped.")


