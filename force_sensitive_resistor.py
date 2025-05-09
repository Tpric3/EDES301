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

ADC.setup()
adc_pin = "P1_21"  # Change to your pin
R_fixed = 10000  # 10kΩ fixed resistor

while True:
    reading = ADC.read(adc_pin)
    voltage = reading * 1.8

    # Skip low voltage readings to avoid division by zero
    if voltage < 0.01 or voltage >= 1.8:
        force = 0.0
    else:
        try:
            resistance = (1.8 - voltage) * R_fixed / voltage
            if resistance == 0:
                force = 0.0
            else:
                force = 1.0 / resistance  # or scale this as needed
        except ZeroDivisionError:
            force = 0.0

    print(f"Force (arb. units): {force:.5f}")
    time.sleep(0.1)


