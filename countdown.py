import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import time
import RPi.GPIO as GPIO

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.attributes("-fullscreen", True)  # Make the application fullscreen

        # Load the background image
        self.bg_image = Image.open("bg.jpg")
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.resize_background)

        # Timer display
        self.time_left = 30 * 60  # 30 minutes in seconds
        self.running = False
        self.blink = False

        # Custom font for the timer
        self.timer_font = font.Font(family="Helvetica", size=480, weight="bold")
        self.timer_outline = []
        self.timer_text_items = []

        # Setup GPIO for button
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button connected to GPIO 17 with pull-up resistor

        # Start polling for button press
        self.poll_button()

        # Update the UI
        self.update_ui()

    def resize_background(self, event):
        # Resize the background to fill the window
        self.canvas.delete("all")
        resized_image = self.bg_image.resize((event.width, event.height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        # Recreate timer text
        self.redraw_timer_text(event.width, event.height)

    def redraw_timer_text(self, width, height):
        # Clear existing text
        for item in self.timer_outline + self.timer_text_items:
            self.canvas.delete(item)

        # Calculate the center of the window
        x_center, y_center = width // 2, height // 2

        # Draw text outlines
        self.timer_outline = []
        for offset in [(-4, -4), (-4, 4), (4, -4), (4, 4)]:
            self.timer_outline.append(
                self.canvas.create_text(
                    x_center + offset[0],
                    y_center + offset[1],
                    text=self.format_time(),
                    fill="black", font=self.timer_font
                )
            )

        # Draw main timer text
        self.timer_text_items = [
            self.canvas.create_text(
                x_center, y_center, text=self.format_time(),
                fill="white", font=self.timer_font
            )
        ]

    def format_time(self):
        minutes, seconds = divmod(self.time_left, 60)
        return f"{minutes:02}:{seconds:02}"

    def toggle_timer(self):
        print("Button pressed")  # Debugging log
        if not self.running:
            self.running = True
            self.update_timer()
        else:
            self.reset_timer()

    def reset_timer(self):
        self.time_left = 30 * 60
        self.running = False
        self.update_ui()

    def update_timer(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.update_ui()
            self.root.after(1000, self.update_timer)

    def update_ui(self):
        # Update the time display
        time_text = self.format_time()
        for outline in self.timer_outline:
            self.canvas.itemconfig(outline, text=time_text)
        for text_item in self.timer_text_items:
            self.canvas.itemconfig(text_item, text=time_text)

        # Handle flashing effect for the last 5 minutes
        if self.time_left <= 5 * 60:
            self.blink = not self.blink
            color = "red" if self.blink else "white"
            for text_item in self.timer_text_items:
                self.canvas.itemconfig(text_item, fill=color)
        else:
            for text_item in self.timer_text_items:
                self.canvas.itemconfig(text_item, fill="white")

    def poll_button(self):
        # Poll the button state and trigger toggle_timer if pressed
        if GPIO.input(17) == GPIO.LOW:  # Button pressed (active low)
            self.toggle_timer()
        self.root.after(100, self.poll_button)  # Poll every 100ms

    def cleanup_gpio(self):
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = CountdownTimer(root)
        root.mainloop()
    except KeyboardInterrupt:
        # Handle cleanup on exit
        print("Exiting...")
        app.cleanup_gpio()
