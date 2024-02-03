#!/usr/bin/python3

# idle_warning.py
import time
import signal
import subprocess
import tkinter as tk
from pynput import mouse, keyboard

# Create a window with a countdown label
window = tk.Tk()
window.title("Idle Warning")
window.geometry("200x100")
window.attributes("-topmost", True)
label = tk.Label(window, text="Screen will lock in 10 seconds", font=("Arial", 16))
label.pack()

# Define a function to update the label and close the window
def update_label():
    global i
    i -= 1
    if i > 0:
        label.config(text=f"Screen will lock in {i} seconds")
        window.after(1000, update_label)
    else:
        window.destroy()

# Define a function to close the window on user input
def close_window(*args):
    window.destroy()

# Define a function to exit the program on SIGUSR1 signal
def exit_program(signum, frame):
    window.destroy()
    exit(0)

# Register the signal handler
signal.signal(signal.SIGUSR1, exit_program)

# Start the countdown
i = 10
window.after(1000, update_label)

# Listen for mouse and keyboard events
mouse_listener = mouse.Listener(on_click=close_window)
keyboard_listener = keyboard.Listener(on_press=close_window)
mouse_listener.start()
keyboard_listener.start()

# Run the main loop
window.mainloop()
