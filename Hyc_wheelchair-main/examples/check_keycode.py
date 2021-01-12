import threading
import keyboard
import time
import numpy as np
import sys
from bluetooth.ble import GATTRequester


STOP = 0
MOVE_FWD = 1
MOVE_BWD = 2
MOVE_R = 3
MOVE_L = 4
F = 5
L = 6



state = 0
keycode = ""
def print_pressed_keys(e):
	global keycode
	keycode = str([str(code) for code in keyboard._pressed_events])
	keycode = keycode[2:-2]
def func1():
	global keycode
	global state
	while(1):
		keyboard.hook(print_pressed_keys)
		print(keycode)

if __name__ == "__main__":
	global state
	t = threading.Thread(target=func1)
	t.start()
	t2 = threading.Thread(target=bleconnect)
	t2.start()
	while(1):
		time.sleep(1)
		
	

