import sys, time
import threading
import keyboard
import numpy as np
from bledevice import scanble, BLEDevice

Device1 = BLEDevice("DD:43:89:16:43:81")
Device2 = BLEDevice("F4:82:B3:50:ED:55")
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
Mon = 7
Moff = 8
keycode = ""
def print_key():
	print("hotkey press")

direction = 1
state = STOP;
'''
def data_ON():
	print("\nData ON")
	Device1.writereq(0xd,'545457550D0A') #RUN_flag
	Device2.writereq(0xd,'545457550D0A') #RUN_flag
def data_OFF():
	print("\nData OFF")
	Device1.writereq(0xd,'545446660D0A') #RUN_flag
	Device2.writereq(0xd,'545446660D0A') #RUN_flag
'''
def motor_OFF():
	global state
	global Device1
	global Device2
	#state = Moff

	Device1.writereq(0xd,'54534F5E0D0A') #break on
	Device2.writereq(0xd,'54534F5E0D0A') #break on
	
	Device1.writereq(0xd,'545246680D0A') #motor off
	Device2.writereq(0xd,'545246680D0A') #motor off
	
def motor_ON():
	global state
	#state = Mon
	Device1.writereq(0xd,'544443790D0A')#CW forward
	Device2.writereq(0xd,'544443790D0A')#CW forward
	Device1.writereq(0xd,'54570A9F0D0A') #1km
	Device2.writereq(0xd,'54570A9F0D0A') #1km
	Device1.writereq(0xd,'54524F5F0D0A') #motor on
	Device2.writereq(0xd,'54524F5F0D0A') #motor on
	Device1.writereq(0xd,'54570A9F0D0A') #1km
	Device2.writereq(0xd,'54570A9F0D0A') #1km
	
def M_FWD():
	global state
	global direction
	#state = MOVE_FWD
	
	Device1.writereq(0xd,'544443790D0A')#CW forward
	Device2.writereq(0xd,'544443790D0A')#CW forward

	Device1.writereq(0xd,'54570A9F0D0A') #1km
	Device2.writereq(0xd,'54570A9F0D0A') #1km
	Device1.writereq(0xd,'54571E8B0D0A')#3km/h
	Device2.writereq(0xd,'54571E8B0D0A')#3km/h
	
def M_FWD_RIGHT():
	global state
	#state = MOVE_FWR_R
	print("\nM_FWD_RIGHT")
def M_FWD_LEFT():
	global state
	#state = MOVE_FWR_L
	print("\nM_FWD_LEFT")

def TURN_RIGHT():
	global state

def TURN_LEFT():
	global state

def GEAR_UP():
	global state

def GEAR_DOWN():
	global state

def M_IDLE():
	global state
	state = IDLE
	
	#motor_ON()
	#print("MOTOR IDLE\n");
	Device1.writereq(0xd,'545714950D0A')#2km/h
	Device2.writereq(0xd,'545714950D0A')#2km/h
	#time.sleep(0.01)
	
def M_BWD():
	global state
	global direction
	state = MOVE_BWD

	Device1.writereq(0xd,'544457650D0A')#CCW backward
	Device2.writereq(0xd,'544457650D0A')#CCW backward
	Device1.writereq(0xd,'545708A10D0A')#0.8km/h
	Device2.writereq(0xd,'545708A10D0A')#0.8km/h
	
def M_RIGHT():
	global state
	state = MOVE_R

	
	Device1.writereq(0xd,'545714950D0A')#2km/h
	Device2.writereq(0xd,'54571E8B0D0A')#3km/h
	
def M_LEFT():
	global state
	state = MOVE_L
	
	Device1.writereq(0xd,'54571E8B0D0A')#3km/h
	Device2.writereq(0xd,'545714950D0A')#2km/h
	
def M_STOP():
	global state
	state = STOP
	
#	Device1.writereq(0xd,'54570A9F0D0A') #1km
#	Device2.writereq(0xd,'54570A9F0D0A') #1km
#	Device1.writereq(0xd,'54534F5E0D0A') #break on
#	Device2.writereq(0xd,'54534F5E0D0A') #break on
	Device1.writereq(0xd,'545700A90D0A') #spd down
	Device2.writereq(0xd,'545700A90D0A') #spd down

'''
	desired = 
	print("Desired Speed = ",desired,'\n');
	desired_temp =format(desired,'X')
	desired_speed = desired_temp[0]+desired_temp[1]
	check_sum_temp = format(0xA9-desired,'X')
	check_sum = check_sum_temp[0]+check_sum_temp[1]
	senddata = "5457"+desired_speed+check_sum+"0D0A";
	
	Device1.writereq(0xd,senddata)#Desired Speed
	Device2.writereq(0xd,senddata)#Desired Speed
'''

'''
def Desired_Speed(direction,desired):
	print("Desired Speed = ",desired,'\n');
	desired_temp =format(desired,'X')
	desired_speed = desired_temp[0]+desired_temp[1]
	check_sum_temp = format(0xA9-desired,'X')
	check_sum = check_sum_temp[0]+check_sum_temp[1]
	senddata = "5457"+desired_speed+check_sum+"0D0A";
	
	#Device1.writereq(0xd,senddata)#Desired Speed
	#Device2.writereq(0xd,senddata)#Desired Speed
	
	print("Senddata = ",senddata,'\n');
'''


def func1():
	keyboard.add_hotkey('w', M_FWD)
	keyboard.add_hotkey('a', M_LEFT)
	keyboard.add_hotkey('s', M_BWD)
	keyboard.add_hotkey('d', M_RIGHT)
	keyboard.add_hotkey('q', M_FWD_LEFT)
	keyboard.add_hotkey('e', M_FWD_RIGHT)
	keyboard.add_hotkey('right', TURN_RIGHT)
	keyboard.add_hotkey('left', TURN_LEFT)
	keyboard.add_hotkey('up', GEAR_UP)
	keyboard.add_hotkey('down', GEAR_DOWN)
	keyboard.add_hotkey('space', M_STOP)
	keyboard.add_hotkey('esc', motor_OFF)
	keyboard.add_hotkey('g', motor_ON)
	#keyboard.add_hotkey('o', Desired_Speed,args=(1,20))

if __name__ == "__main__":
	t = threading.Thread(target=func1)
	t.start()
	while True:

		time.sleep(0.1)

