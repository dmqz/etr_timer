from gpiozero import Button
from signal import pause

button = Button(17, pull_up=False)

def button_pressed():
    print("Button was pushed!")

button.when_pressed = button_pressed

print("Waiting for button press...")
pause()
