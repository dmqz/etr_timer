import lgpio
import time

# Initialize the GPIO
gpio = lgpio.gpiochip_open(0)  # Open the first GPIO chip (usually GPIO 0 on Raspberry Pi)

# Define the GPIO pin to which the button is connected
button_pin = 17  # Replace with the actual pin number

# Set the pin as input with a pull-up resistor (lgpio.PUD_UP)
lgpio.gpio_claim_input(gpio, button_pin, pull=lgpio.PUD_UP)  # Set GPIO 17 as input with pull-up resistor

# Define the callback function for button press
def button_pressed(gpio, pin, level, tick):
    if level == lgpio.LOW:
        print("Button pressed!")

# Set up event detection on falling edge (button press)
lgpio.gpio_event(gpio, button_pin, lgpio.FALLING_EDGE, button_pressed)

try:
    while True:
        time.sleep(1)  # Wait indefinitely, event detection will handle button press
except KeyboardInterrupt:
    pass  # Handle the keyboard interrupt gracefully
finally:
    lgpio.gpiochip_close(gpio)  # Close the GPIO chip and clean up
