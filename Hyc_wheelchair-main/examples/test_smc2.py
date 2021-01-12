import sys, time
import threading
import keyboard
import numpy as np

from gattlib import GATTRequester, GATTResponse
#Device1 = GATTRequester("40:06:A0:97:74:A9", False) # right wheel
#Device2 = GATTRequester("40:06:A0:94:FE:F7", False) # left wheel
Device1 = GATTRequester("DD:43:89:16:43:81", False) # right wheel
Device2 = GATTRequester("F4:82:B3:50:ED:55", False) # left wheel'
time.sleep(0.5)
sum_time = 0;
mean_time = 0;
count = 0;

STOP = 0
MOVE_FWD = 1
MOVE_BWD = 2
MOVE_FWR_R = 10
MOVE_FWR_L = 11

MOVE_R = 3
MOVE_L = 4
IDLE = 9
F = 5
S = 6
Mon = 7
Moff = 8
keycode = ""
def print_key():
	print("hotkey press")

direction = 1
state = STOP;
def print_state():
	global state
	if state == MOVE_FWD:
		print("\nMOVE_FORWARD")
	elif state == MOVE_BWD:
		print("\nMOVE_BACKWARD")
	elif state == MOVE_R:
		print("\nMOVE_RIGHT")
	elif state == MOVE_L:
		print("\nMOVE_LEFT")
	elif state == STOP:
		M_STOP();
		print("\nSTOP")
	elif state == F:
		print("\nSTOP")
	elif state == S:
		print("\nSTOP")
	elif state == Mon:
		print("\nMOTOR_ON")
	elif state == Moff:
		print("\nMOTOR_OFF")
	elif state == IDLE:
		M_IDLE()
		print("\nIDLE")
	
def data_ON():
	print("\nData ON")
	'''
	Device1.write_by_handle(0xd,b'\x54545755\x0D\x0A') #RUN_flag
	Device2.write_by_handle(0xd,b'\x54545755\x0D\x0A') #RUN_flag
	'''
def data_OFF():

	print("\nData OFF")
	'''
	Device1.write_by_handle(0xd,b'\x54544666\x0D\x0A') #RUN_flag
	Device2.write_by_handle(0xd,b'\x54544666\x0D\x0A') #RUN_flag
	'''
def motor_OFF():
	global state
	global Device1
	global Device2
	state = Moff
	
	Device1.write_by_handle(0xd,b'\x54\x52\x46\x68\x0D\x0A') #RUN_flag
	Device2.write_by_handle(0xd,b'\x54\x52\x46\x68\x0D\x0A') #RUN_flag
	
def motor_ON():
	global state
	state = Mon
	
	Device1.write_by_handle(0xd,b'\x54\x52\x4F\x5F\x0D\x0A') #RUN_flag
	Device2.write_by_handle(0xd,b'\x54\x52\x4F\x5F\x0D\x0A') #RUN_flag
	
def M_FWD():
	global state
	global direction
	state = MOVE_FWD
	
	if direction == -1:
		M_STOP();
		time.sleep(0.2)
		Device1.write_by_handle(0xd,b'\x54\x44\x43\x79\x0D\x0A')#CCW forward
		Device2.write_by_handle(0xd,b'\x54\x44\x43\x79\x0D\x0A')#CCW forward
		direction = 1;
		motor_ON();
		M_IDLE()
	Device1.write_by_handle(0xd,b'\x54\x57\x50\x59\x0D\x0A')#5km/h
	Device2.write_by_handle(0xd,b'\x54\x57\x50\x59\x0D\x0A')#5km/h
	
def M_FWD_RIGHT():
	global state
	state = MOVE_FWR_R
	print("\nM_FWD_RIGHT")
def M_FWD_LEFT():
	global state
	state = MOVE_FWR_L
	print("\nM_FWD_LEFT")

def M_IDLE():
	global state
	state = IDLE
	
	#motor_ON()
	#print("MOTOR IDLE\n");
	Device1.write_by_handle(0xd,b'\x54\x57\x14\x95\x0D\x0A');#2km/h;
	Device2.write_by_handle(0xd,b'\x54\x57\x14\x95\x0D\x0A')#2km/h
	
def M_BWD():
	global state
	global direction
	state = MOVE_BWD
	if direction == 1:
		M_STOP();
		time.sleep(0.2)
		Device1.write_by_handle(0xd,b'\x54\x44\x57\x65\x0D\x0A')#CW backward
		Device2.write_by_handle(0xd,b'\x54\x44\x57\x65\x0D\x0A')#CW backward
		direction = -1;
		motor_ON();
		M_IDLE()
	Device1.write_by_handle(0xd,b'\x54\x57\x08\xA1\x0D\x0A')#0.8km/h
	Device2.write_by_handle(0xd,b'\x54\x57\x08\xA1\x0D\x0A')#0.8km/h
	
def M_RIGHT():
	global state
	state = MOVE_R

	
	Device1.write_by_handle(0xd,b'\x54\x57\x14\x95\x0D\x0A')#2km/h
	Device2.write_by_handle(0xd,b'\x54\x57\x32\x77\x0D\x0A')#5km/h
	
def M_LEFT():
	global state
	state = MOVE_L
	
	Device1.write_by_handle(0xd,b'\x54\x57\x32\x77\x0D\x0A')#5km/h
	Device2.write_by_handle(0xd,b'\x54\x57\x14\x95\x0D\x0A')#2km/h
	
def M_STOP():
	global state
	state = STOP
	
	Device1.write_by_handle(0xd,b'\x54\x57\x00\xA9\x0D\x0A')#0km/h
	Device2.write_by_handle(0xd,b'\x54\x57\x00\xA9\x0D\x0A')#0km/h
	
def fFASTER():
	global state
	state = F
	'''
	Device1.write_by_handle(0xd,b'\x54757516\x0D\x0A')#Spd_Up
	Device2.write_by_handle(0xd,b'\x54757516\x0D\x0A')#Spd_Up
	'''
def fSLOWER():
	global state
	state = S
	'''
	Device1.write_by_handle(0xd,b'\x54646438\x0D\x0A')#Spd_Down
	Device2.write_by_handle(0xd,b'\x54646438\x0D\x0A')#Spd_Down
	'''
def Desired_Speed(direction,desired):
	print("Desired Speed = ",desired,'\n');
	desired_temp =format(desired,'X')
	desired_speed = desired_temp[0]+desired_temp[1]
	check_sum_temp = format(0xA9-desired,'X')
	check_sum = check_sum_temp[0]+check_sum_temp[1]
	senddata = "5457"+desired_speed+check_sum+"\x0D\x0A";
	'''
	Device1.write_by_handle(0xd,senddata)#Desired Speed
	Device2.write_by_handle(0xd,senddata)#Desired Speed
	'''
	print("Senddata = ",senddata,'\n');

CONNECTION_OPTIONS_LEGACY_BDADDR_LE_PUBLIC = (1 << 0)
CONNECTION_OPTIONS_LEGACY_BDADDR_LE_RANDOM = (1 << 1)
CONNECTION_OPTIONS_LEGACY_BT_SEC_LOW = (1 << 2)
CONNECTION_OPTIONS_LEGACY_BT_SEC_MEDIUM = (1 << 3)
CONNECTION_OPTIONS_LEGACY_BT_SEC_HIGH = (1 << 4)

keyboard.add_hotkey('w', M_FWD)
keyboard.add_hotkey('a', M_LEFT)
keyboard.add_hotkey('s', M_BWD)
keyboard.add_hotkey('d', M_RIGHT)
keyboard.add_hotkey('w+a', M_FWD_LEFT)
keyboard.add_hotkey('w+d', M_FWD_RIGHT)
keyboard.add_hotkey('space', M_STOP)
keyboard.add_hotkey('esc', motor_OFF)
keyboard.add_hotkey('r', motor_ON)
keyboard.add_hotkey('o', Desired_Speed,args=(1,20))

if __name__ == "__main__":
#	global direction
	sys.stdout.flush()
	Device1.connect(True,'random')
	time.sleep(1)
	Device2.connect(True,'random')
	time.sleep(1)
	print("Connection OK")
	while True:
		#M_IDLE()
		print_state()
		if state == STOP or state == IDLE:
			pass
		else:
			state = IDLE
		print("direction = ",direction);
		time.sleep(0.01)
		'''
		count = count+1;	
		start = time.time() 
		#data = Device1.notify();
		data = 'notify\n';
		sum_time = sum_time + time.time() - start;
		mean_time = sum_time/count;
		print("time :", time.time() - start,"mean_time : ",mean_time,"\n",);
		print(data)
		print("\n")
		'''
