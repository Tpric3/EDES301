from ht16k33 import HT16K33  # Make sure this is your class file
import time

def test_display():
    # Initialize the display with the correct arguments
    display = HT16K33(bus=1, address=0x70)  # Omitting the 'command' parameter as it's optional

    # Test setting a digit
    display.set_digit(0, 1)
    display.set_digit(1, 2)
    display.set_digit(2, 3)
    display.set_digit(3, 4)
    display.set_colon(True)

    # You can add additional tests as needed
    time.sleep(2)  # Wait for 2 seconds to see the display

if __name__ == "__main__":
    test_display()

