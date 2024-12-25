#!/usr/bin/env python3
########################################################################
# Filename    : TimerWithButton.py
# Description : Timer with Button Polling
# Author      : freenove
# modification: 2023/12/25
########################################################################
import time
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
from datetime import datetime

# Initialize the LCD with the correct I2C address (0x3F)
lcd1602 = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=16, rows=2)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button on GPIO17 with internal pull-up resistor

# Setup debounce delay and last button press time
debounce_delay = 0.5  # 500ms debounce delay
last_button_press_time = 0  # Store the last button press time

# Timer settings
timer_duration = 30 * 60  # 30 minutes in seconds
timer_running = False

def start_timer():
    """Start the timer or reset it to 30 minutes and stop it."""
    global timer_running, timer_duration
    if not timer_running:
        # Start the timer if it's not already running
        timer_running = True
        print("Timer started!")
    else:
        # Stop the timer and reset it to 30 minutes
        timer_running = False
        timer_duration = 30 * 60  # Reset to 30 minutes
        print("Timer reset and stopped!")

def poll_button():
    """Poll the button state to detect a press with debounce."""
    global last_button_press_time

    # Get the current time
    current_time = time.time()

    # Only process the button press if enough time has passed since the last press
    if GPIO.input(17) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
        print("Button Pressed!")  # Print message when button is pressed
        start_timer()  # Start or stop/reset the timer
        last_button_press_time = current_time  # Update the last button press time

    # Poll every 100ms (0.1 seconds)
    time.sleep(0.1)

def update_timer():
    """Update the timer and display on the LCD."""
    global timer_duration, timer_running

    if timer_running:
        # Countdown timer display
        minutes = timer_duration // 60
        seconds = timer_duration % 60
        lcd1602.clear()
        lcd1602.write_string(f'Timer: {minutes:02}:{seconds:02}')
        timer_duration -= 1  # Decrease the timer by 1 second
        if timer_duration <= 0:
            lcd1602.clear()
            lcd1602.write_string('Time Up!')
            timer_running = False  # Stop the timer
        time.sleep(1)
    else:
        # When the timer is not running, show 30:00 and wait for activation
        lcd1602.clear()
        lcd1602.write_string('Timer: 30:00')

def main():
    """Main function to continuously poll the button and run the timer."""
    print("Polling started. Press the button to start or reset the timer.")
    try:
        while True:
            poll_button()  # Continuously poll for button press
            update_timer()  # Update and display the timer
    except KeyboardInterrupt:
        print("\nProgram terminated.")
        GPIO.cleanup()  # Cleanup GPIO settings when exiting the program

if __name__ == '__main__':
    main()
