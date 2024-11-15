from pynput import keyboard, mouse
import time
import threading

# Variable to track last input time
last_input_time = time.time()

# Timeout (in seconds) after which you assume no input occurred
timeout = 10

# Callback function for keyboard events
def on_press(key):
    global last_input_time
    last_input_time = time.time()  # Update time when a key is pressed
    print(f"Key {key} pressed")

# Callback function for mouse click events
def on_click(x, y, button, pressed):
    global last_input_time
    last_input_time = time.time()  # Update time when a mouse button is pressed
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")

# Callback function for mouse movement
def on_move(x, y):
    global last_input_time
    last_input_time = time.time()  # Update time when the mouse is moved
    #print(f"Mouse moved to ({x}, {y})")

# Function to monitor the time passed since the last input
def monitor_inactivity():
    global last_input_time
    while True:
        elapsed_time = time.time() - last_input_time
        if elapsed_time > timeout:
            print(f"No input for {timeout} seconds")
            # You can also set a flag here to indicate inactivity
        time.sleep(1)  # Check every second

# Function to check if any input is active
def is_input_active():
    global last_input_time
    elapsed_input_time = time.time() - last_input_time
    print(f"Elapsed input time: {elapsed_input_time:.2f} seconds")  # Debug print
    return elapsed_input_time <= timeout  # Returns True if input was detected within the timeout period

# Start keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# Start mouse listener for clicks and movement
mouse_listener = mouse.Listener(on_click=on_click,on_move=on_move)
mouse_listener.start()

# Start monitoring inactivity in a separate thread
monitor_thread = threading.Thread(target=monitor_inactivity)
monitor_thread.daemon = True  # Allow thread to exit when the main program does
monitor_thread.start()
