import RPi.GPIO as GPIO
import time

# Set the GPIO mode and configure the pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_pressed(channel):
    print("Button pressed!")

# Add event detection for GPIO 17
GPIO.add_event_detect(17, GPIO.FALLING, callback=button_pressed, bouncetime=300)

try:
    while True:
        time.sleep(1)  # Wait indefinitely, event detection will handle button press
except KeyboardInterrupt:
    pass  # Handle the keyboard interrupt gracefully

finally:
    # Clean up GPIO settings on exit
    GPIO.cleanup()
