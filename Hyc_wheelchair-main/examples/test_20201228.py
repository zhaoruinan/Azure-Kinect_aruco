import sys, time
import threading
import keyboard
import numpy as np

from bledevice import scanble, BLEDevice
Device2 = BLEDevice("F4:82:B3:50:ED:55")
Device2.writereq(0xd,'54524F5F0D0A') #RUN_flag

desired = 0
flag = 1;
now_velocity = 0

def M_FWD():
	global now_velocity
	if now_velocity<16:
		now_velocity = 16;
	now_velocity =now_velocity +1; 
	return now_velocity;
def M_BWD():
	global now_velocity
	if now_velocity<16:
		now_velocity = 16;
	now_velocity =now_velocity -1; 
	return now_velocity;
def M_STOP():
	global now_velocity
	now_velocity =0; 
	return now_velocity;

def desired_speed(desired):

	if desired<16:
		print("Desired Speed = ",desired,'\n');
		desired_temp =format(desired,'X')
		desired_speed =format(0,'X')+desired_temp

	else:
		print("Desired Speed = ",desired,'\n');
		desired_temp =format(desired,'X')
		desired_speed = desired_temp[0]+desired_temp[1]
	
	check_sum_temp = format(0xA9-desired,'X')
	check_sum = check_sum_temp[0]+check_sum_temp[1]
	senddata = "5457"+desired_speed+check_sum+"0D0A";
	Device2.writereq(0xd,senddata)#Desired Speed
	Device2.notify()



keyboard.add_hotkey('w', M_FWD)
keyboard.add_hotkey('s', M_BWD)
keyboard.add_hotkey('space', M_STOP)

if __name__ == "__main__":
	desired_speed(10)
	time.sleep(2)
	desired_speed(0)
	while 1:
		now_velocity = now_velocity
		desired = int(now_velocity)
		if desired<0:
			desired = 0;
		if desired>100:
			desired = 100;
		desired_speed(desired)
		time.sleep(0.05)
	
