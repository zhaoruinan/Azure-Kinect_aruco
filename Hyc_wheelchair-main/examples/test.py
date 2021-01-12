import threading
import keyboard
import time
import numpy as np
import sys
from bluetooth.ble import GATTRequester, GATTResponse


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
		elif keycode =='103': #up
			state = F
		elif keycode =='108': #down
			state = S
		elif keycode =='19': #R
			state = Mon
		elif keycode =='1': #esc
			state = Moff
		time.sleep(0.01)
	motor_OFF()
	time.sleep(2)
requester1 = GATTRequester("DD:43:89:16:43:81", False) # right wheel
requester2 = GATTRequester("F4:82:B3:50:ED:55", False) # left wheel'
response = GATTResponse()
def data_ON():
	requester1.write_by_handle(0x0d, b'\x54\x54\x57\x55\x0D\x0A')
	requester2.write_by_handle(0x0d, b'\x54\x54\x57\x55\x0D\x0A')
def data_OFF():
	requester1.write_by_handle(0x0d, b'\x54\x54\x46\x66\x0D\x0A')
	requester2.write_by_handle(0x0d, b'\x54\x54\x46\x66\x0D\x0A')
def motor_OFF():
	requester1.write_by_handle(0x0d, b'\x54\x52\x46\x68\x0D\x0A') #STOP_flag
	requester2.write_by_handle(0x0d, b'\x54\x52\x46\x68\x0D\x0A') #STOP_flag

def motor_ON():
	requester1.write_by_handle(0x0d, b'\x54\x52\x4F\x5F\x0D\x0A') #RUN_flag
	requester2.write_by_handle(0x0d, b'\x54\x52\x4F\x5F\x0D\x0A') #RUN_flag
def read_data():
	print("receive --\n")
	#requester1.read_by_handle_async(0x0d, self.response)
	#data = self.response.received()[0]
	#print("received: ",data)

def M_FWD():

	#motor_ON()
	if direction == -1:
		time.sleep(0.2)
		requester1.write_by_handle(0x0d, b'\x54\x44\x43\x79\x0D\x0A') #CCW forward
		requester2.write_by_handle(0x0d, b'\x54\x44\x43\x79\x0D\x0A') #CCW forward
		direction = 1;
		motor_ON();
		M_IDLE()
	requester1.write_by_handle(0x0d, b'\x54\x57\x50\x59\x0D\x0A') #5km/h
	requester2.write_by_handle(0x0d, b'\x54\x57\x50\x59\x0D\x0A') #5km/h
def M_IDLE():
	#motor_ON()
	#print("MOTOR IDLE\n");


	requester1.write_by_handle(0x0d, b'\x54\x57\x14\x95\x0D\x0A') #2km/h
	requester2.write_by_handle(0x0d, b'\x54\x57\x14\x95\x0D\x0A') #2km/h

def M_BWD():
	#motor_ON()

	if direction == 1:
		time.sleep(0.2)
		requester1.write_by_handle(0x0d, b'\x54\x44\x57\x65\x0D\x0A') #CW backward
		requester2.write_by_handle(0x0d, b'\x54\x44\x57\x65\x0D\x0A') #CW backward
		direction = -1;
		motor_ON();
		M_IDLE()
	requester1.write_by_handle(0x0d, b'\x54\x57\x08\xA1\x0D\x0A') #0.8km/h
	requester2.write_by_handle(0x0d, b'\x54\x57\x08\xA1\x0D\x0A') #0.8km/h
def M_RIGHT():

	#motor_ON()
	#requester1.write_by_handle(0x0d, b'\x54\x44\x43\x79\x0D\x0A') #CCW forward
	#requester2.write_by_handle(0x0d, b'\x54\x44\x43\x79\x0D\x0A') #CCW forward
	requester1.write_by_handle(0x0d, b'\x54\x57\x14\x95\x0D\x0A') #2km/h
	requester2.write_by_handle(0x0d, b'\x54\x57\x32\x77\x0D\x0A') #5km/h
	#time.sleep(3)
	#state=STOP
def M_LEFT():

	#motor_ON()
	#requester1.write_by_handle(0x0d, b'\x54\x44\x43\x79\x0D\x0A') #CCW forward
	#requester2.write_by_handle(0x0d, b'\x54\x44\x43\x79\x0D\x0A') #CCW forward
	requester1.write_by_handle(0x0d, b'\x54\x57\x32\x77\x0D\x0A') #5km/h
	requester2.write_by_handle(0x0d, b'\x54\x57\x14\x95\x0D\x0A') #2km/h
	#time.sleep(3)
	#state=STOP
def M_STOP():
        requester1.write_by_handle(0x0d, b'\x54\x57\x00\xA9\x0D\x0A') #0km/h
        requester2.write_by_handle(0x0d, b'\x54\x57\x00\xA9\x0D\x0A') #0km/h
def fFASTER():
        requester1.write_by_handle(0x0d, b'\x54\x75\x75\x16\x0D\x0A') #Spd_UP
        requester2.write_by_handle(0x0d, b'\x54\x75\x75\x16\x0D\x0A') #Spd_UP
def fSLOWER():
        requester1.write_by_handle(0x0d, b'\x54\x64\x64\x38\x0D\x0A') #Spd_DOWN
        requester2.write_by_handle(0x0d, b'\x54\x64\x64\x38\x0D\x0A') #Spd_DOWN


def bleconnect():

	sys.stdout.flush()
	requester1.connect(True,'random')
	time.sleep(1)
	requester2.connect(True,'random')
	time.sleep(1)
	print("CONNECTION IS COMPLETE")

	motor_OFF()
	motor_ON()
	data_OFF()
	state = IDLE
	while(1):
		if state == MOVE_FWD:
			M_FWD()
			time.sleep(0.01)
			state = IDLE;
			print("W")
		elif state == MOVE_BWD:
			M_BWD()
			time.sleep(0.01)
			state = IDLE;
			print("S")
		elif state == MOVE_R:
			M_RIGHT()
			time.sleep(0.01)
			state = IDLE;
			print("D")
		elif state == MOVE_L:
			M_LEFT()
			time.sleep(0.01)
			state = IDLE;
			print("A")
		elif state == STOP:
			time.sleep(0.01)
			M_STOP()
			print("spacebar")
		elif state == F:
			fFASTER()
			time.sleep(0.01)
			state = IDLE;
			print("spd_up")
		elif state == S:
			fSLOWER()
			time.sleep(0.01)
			state = IDLE;
			print("spd_down")
		elif state == Mon:
			motor_ON()
			time.sleep(0.01)
			state = IDLE;
			print("motor_ON")
		elif state == Moff:
			time.sleep(0.01)
			state = IDLE;
			motor_OFF()
			print("motor_OFF")
		elif state == IDLE:
			pass;
		time.sleep(0.01)

if __name__ == "__main__":


	t = threading.Thread(target=func1)
	t.start()
	t2 = threading.Thread(target=bleconnect)
	t2.start()
	while(1):
		#print("state = ",state,"direction  = ",direction);
		#print("\n")
		time.sleep(0.01)
		
	
