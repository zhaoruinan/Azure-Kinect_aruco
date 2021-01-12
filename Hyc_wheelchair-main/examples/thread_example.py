import threading
import keyboard
import time
import numpy as np
import sys
import sys, time
from bledevice import scanble, BLEDevice

STOP = 0
MOVE_FWD = 1
MOVE_BWD = 2
MOVE_R = 3
MOVE_L = 4
IDLE = 9
F = 5
S = 6
Mon = 7
Moff = 8


direction = 1;

state = 0
keycode = ""
Device1 = BLEDevice("DD:43:89:16:43:81")
Device2 = BLEDevice("F4:82:B3:50:ED:55")

def print_pressed_keys(e):
	global keycode
	keycode = str([str(code) for code in keyboard._pressed_events])
	keycode = keycode[2:-2]
def func1():
	global keycode

	keyboard.hook(print_pressed_keys)
	while(1):
		
		if keycode =='17': #W
			state = MOVE_FWD
		elif keycode =='31': #S
			state = MOVE_BWD
		elif keycode =='32': #D
			state = MOVE_R
		elif keycode =='30': #A
			state = MOVE_L
		elif keycode =='57': #spacebar
			state = STOP
		elif keycode =='19': #R
			state = Mon
		elif keycode =='1': #esc
			state = Moff
		time.sleep(0.01)
	motor_OFF()
	time.sleep(2)

def data_ON():
	Device1.writereq(0xd,'545457550D0A') #RUN_flag
	Device2.writereq(0xd,'545457550D0A') #RUN_flag
def data_OFF():
	Device1.writereq(0xd,'545446660D0A') #RUN_flag
	Device2.writereq(0xd,'545446660D0A') #RUN_flag
def motor_OFF():
	Device1.writereq(0xd,'545246680D0A') #RUN_flag
	Device2.writereq(0xd,'545246680D0A') #RUN_flag

def motor_ON():
	Device1.writereq(0xd,'54524F5F0D0A') #RUN_flag
	Device2.writereq(0xd,'54524F5F0D0A') #RUN_flag
def read_data():
	print("receive --\n")
	#requester1.read_by_handle_async(0x0d, self.response)
	#data = self.response.received()[0]
	#print("received: ",data)

def M_FWD():
	#motor_ON()
	print("M_FWD")
	global direction
	if direction == -1:
		time.sleep(0.2)
		Device1.writereq(0xd,'544443790D0A')#CCW forward
		Device2.writereq(0xd,'544443790D0A')#CCW forward
		direction = 1;
	Device1.writereq(0xd,'545714950D0A')#2km/h
	Device2.writereq(0xd,'545714950D0A')#2km/h
def M_IDLE():
	#motor_ON()
	#print("MOTOR IDLE\n");
	Device1.writereq(0xd,'545705A40D0A')#2km/h
	Device2.writereq(0xd,'545705A40D0A')#2km/h

def M_BWD():
	#motor_ON()
	global direction
	if direction == 1:
		time.sleep(0.2)
		Device1.writereq(0xd,'544457650D0A')#CW backward
		Device2.writereq(0xd,'544457650D0A')#CW backward
		direction = -1;
	Device1.writereq(0xd,'545714950D0A')#2km/h
	Device2.writereq(0xd,'545714950D0A')#2km/h

def M_RIGHT():
	Device1.writereq(0xd,'545714950D0A')#2km/h
	Device2.writereq(0xd,'545732770D0A')#5km/h
def M_LEFT():
	Device1.writereq(0xd,'545732770D0A')#5km/h
	Device2.writereq(0xd,'545714950D0A')#2km/h
def M_STOP():
	Device1.writereq(0xd,'545700A90D0A')#0km/h
	Device2.writereq(0xd,'545700A90D0A')#0km/h
def fFASTER():
	Device1.writereq(0xd,'547575160D0A')#Spd_Up
	Device2.writereq(0xd,'547575160D0A')#Spd_Up
def fSLOWER():
	Device1.writereq(0xd,'546464380D0A')#Spd_Down
	Device2.writereq(0xd,'546464380D0A')#Spd_Down
keyboard.add_hotkey('w', M_FWD)
keyboard.add_hotkey('a', M_LEFT)
keyboard.add_hotkey('s', M_BWD)
keyboard.add_hotkey('d', M_RIGHT)
keyboard.add_hotkey('space', M_STOP)
keyboard.add_hotkey('esc', motor_OFF)
keyboard.add_hotkey('r', motor_ON)

def bleconnect():
	motor_OFF()
	motor_ON()
	data_OFF()
	state = IDLE
	while(1):
		
		time.sleep(0.1)

if __name__ == "__main__":


	t = threading.Thread(target=func1)
	t.start()
	t2 = threading.Thread(target=bleconnect)
	t2.start()
	while(1):
		#print("state = ",state,"direction  = ",direction);
		#print("\n")
		time.sleep(0.01)
		
	
