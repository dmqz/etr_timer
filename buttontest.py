#!/usr/bin/env python3
########################################################################
# Filename    : ButtonPoller.py
# Description : Simple button press detection using polling method
# Author      : freenove
# modification: 2023/12/25
########################################################################
import time
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button on GPIO17 with internal pull-up resistor

# Setup debounce delay and last button press time
debounce_delay = 0.5  # 500ms debounce delay
last_button_press_time = 0  # Store the last button press time

def poll_button():
    """Poll the button state to detect a press with debounce."""
    global last_button_press_time

    # Get the current time
    current_time = time.time()

    # Only process the button press if enough time has passed since the last press
    if GPIO.input(17) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
        print("Button Pressed!")  # Print message when button is pressed
        last_button_press_time = current_time  # Update the last button press time

    # Poll every 100ms (0.1 seconds)
    time.sleep(0.1)

def main():
    """Main function to continuously poll the button."""
    print("Button Polling started. Press the button to see the message.")
    try:
        while True:
            poll_button()  # Continuously poll for button press
    except KeyboardInterrupt:
        print("\nProgram terminated.")
        GPIO.cleanup()  # Cleanup GPIO settings when exiting the program

if __name__ == '__main__':
    main()
