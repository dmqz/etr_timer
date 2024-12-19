import lgpio
import time

# Initialize the GPIO
gpio = lgpio.gpiochip(0)  # Use the first GPIO chip (usually GPIO 0 on Raspberry Pi)

# Define the GPIO pin to which the button is connected
button_pin = 17  # Replace with the actual pin number

# Set the pin as input with a pull-up resistor
lgpio.gpion( gpio, button_pin, lgpio.INPUT)  # Set GPIO 17 as input
lgpio.set_pullup(gpio, button_pin)  # Enable internal pull-up resistor

# Define the callback function for button press
def button_pressed(gpio, pin, level, tick):
    if level == lgpio.LOW:
        print("Button pressed!")

# Set up event detection on falling edge (button press)
lgpio.event_detect(gpio, button_pin, lgpio.FALLING_EDGE, button_pressed)

try:
    while True:
        time.sleep(1)  # Wait indefinitely, event detection will handle button press
except KeyboardInterrupt:
    pass  # Handle the keyboard interrupt gracefully
finally:
    lgpio.close(gpio)  # Clean up and close the GPIO chip
