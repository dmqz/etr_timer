import RPi.GPIO as GPIO
import time

# Set up GPIO numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin to which the button is connected
button_pin = 17  # Replace with the actual pin number

# Set the pin as input with a pull-up resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Read the button state
        button_state = GPIO.input(button_pin)

        # If the button is pressed (LOW state because of pull-up resistor)
        if button_state == GPIO.LOW:
            print("Button Pressed")
            # Add code here to perform actions when the button is pressed
            time.sleep(0.3)  # Debounce delay

        time.sleep(0.1)  # Check every 100ms

except KeyboardInterrupt:
    # Clean up GPIO settings on exit
    GPIO.cleanup()
