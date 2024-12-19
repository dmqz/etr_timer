import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

def button_callback(channel):
    print("Button was pushed!")

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set GPIO pin 17 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(17, GPIO.RISING, callback=button_callback)  # Setup event on GPIO pin 17 rising edge

message = input("Press enter to quit\n\n")  # Run until someone presses enter

GPIO.cleanup()  # Clean up
