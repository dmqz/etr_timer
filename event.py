from gpiozero import Button
from signal import pause

# Define the button on GPIO 17
button = Button(17, pull_up=False)  # pull_up=False enables internal pull-down resistor

# Callback function for button press
def button_pressed():
    print("Button was pushed!")

# Attach the callback to the button's "when_pressed" event
button.when_pressed = button_pressed

print("Press the button to trigger the event. Press Ctrl+C to exit.")
pause()  # Keeps the script running
