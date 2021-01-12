import numpy as np
import cv2
import cv2.aruco as aruco
#from aruco_lib import *
import time
import pyrealsense2 as rs
import copy
import threading

import sys, time
import threading
import keyboard
import numpy as np

from bledevice import scanble, BLEDevice
Device1 = BLEDevice("DD:43:89:16:43:81") #right wheel
Device2 = BLEDevice("F4:82:B3:50:ED:55") #left  wheel
Device1.writereq(0xd,'54524F5F0D0A') #RUN_flag
Device1.notify()
Device2.writereq(0xd,'54524F5F0D0A') #RUN_flag
Device2.notify()
Device1.writereq(0xd,'544443790D0A') #FRONT
Device1.notify()
Device2.writereq(0xd,'544443790D0A') #FRONT
Device2.notify()
desired = 0
flag = 1;
now_velocity1 = 0
now_velocity2 = 0

STOP = 0;
IDLE = 1;
FWD= 2;
LEFT = 3;
RIGHT = 4;
ROTATE = 6;

direction1 = 1
direction2 = 1
state = STOP
GEAR = 1;
def M_IDLE():
	global now_velocity1
	global now_velocity2
	global direction1
	global direction2
	global state
	global GEAR

#	if direction1 == -1:
#		Device1.writereq(0xd,'544443790D0A') #FRONT
#		Device1.notifyw()
#		direction1 = 1;
#	if direction2 == -1:
#		Device2.writereq(0xd,'544443790D0A') #FRONT	
#		Device1.notify()
#		direction2 = 1;
	if GEAR == 1:
		now_velocity1 = 8;
		now_velocity2 = 8;
	if GEAR == 2:
		now_velocity1 = 16;
		now_velocity2 = 16;
	if GEAR == 3:
		now_velocity1 = 24;
		now_velocity2 = 24;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));
	print("IDLE")
	state = IDLE

def M_STOP():
	global now_velocity1
	global now_velocity2
	global state
	now_velocity1 = 0;
	now_velocity2 = 0;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));
	state = STOP

def M_LEFT():
	global now_velocity1
	global now_velocity2
	global direction1
	global direction2
	global state
	global GEAR
	if direction1 == -1:
		Device1.writereq(0xd,'544443790D0A') #FRONT
		Device1.notifyw()
		direction1 = 1;
	if direction2 == -1:
		Device2.writereq(0xd,'544443790D0A') #FRONT	
		Device1.notify()
		direction2 = 1;
	if GEAR == 1:
		now_velocity1 = 35;
		now_velocity2 = 6;
	if GEAR == 2:
		now_velocity1 = 30;
		now_velocity2 = 10;
	if GEAR == 3:
		now_velocity1 = 25;
		now_velocity2 = 15;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));
	state = IDLE
def M_LEFT2():
	global now_velocity1
	global now_velocity2
	global direction1
	global direction2
	global state
	global GEAR
	if direction1 == -1:
		Device1.writereq(0xd,'544443790D0A') #FRONT
		Device1.notifyw()
		direction1 = 1;
	if direction2 == -1:
		Device2.writereq(0xd,'544443790D0A') #FRONT	
		Device1.notify()
		direction2 = 1;
	if GEAR == 1:
		now_velocity1 = 16;
		now_velocity2 = 10;
	if GEAR == 2:
		now_velocity1 = 24;
		now_velocity2 = 18;
	if GEAR == 3:
		now_velocity1 = 32;
		now_velocity2 = 26;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));
	state = IDLE

def M_RIGHT():
	global now_velocity1
	global now_velocity2
	global direction1
	global direction2
	global GEAR
	if direction1 == -1:
		Device1.writereq(0xd,'544443790D0A') #FRONT
		Device1.notifyw()
		direction1 = 1;
	if direction2 == -1:
		Device2.writereq(0xd,'544443790D0A') #FRONT	
		Device1.notify()
		direction2 = 1;
	if GEAR == 1:
		now_velocity2 = 35;
		now_velocity1 = 6;
	if GEAR == 2:
		now_velocity2 = 30;
		now_velocity1 = 10;
	if GEAR == 3:
		now_velocity2 = 25;
		now_velocity1 = 15;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));
def M_RIGHT2():
	global now_velocity1
	global now_velocity2
	global direction1
	global direction2
	global GEAR
	if direction1 == -1:
		Device1.writereq(0xd,'544443790D0A') #FRONT
		Device1.notifyw()
		direction1 = 1;
	if direction2 == -1:
		Device2.writereq(0xd,'544443790D0A') #FRONT	
		Device1.notify()
		direction2 = 1;
	if GEAR == 1:
		now_velocity2 = 16;
		now_velocity1 = 10;
	if GEAR == 2:
		now_velocity2 = 24;
		now_velocity1 = 18;
	if GEAR == 3:
		now_velocity2 = 32;
		now_velocity1 = 26;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));

def M_FWD():
	global now_velocity1
	global now_velocity2
	global direction1
	global direction2
	global state
	global GEAR
	if direction1 == -1:
		Device1.writereq(0xd,'544443790D0A') #FRONT
		Device1.notify()
		direction1 = 1;
	if direction2 == -1:
		Device2.writereq(0xd,'544443790D0A') #FRONT
		Device1.notify()	
		direction2 = 1;
	if GEAR == 1:
		now_velocity1 = 16;
		now_velocity2 = 16;
	if GEAR == 2:
		now_velocity1 = 24;
		now_velocity2 = 24;
	if GEAR == 3:
		now_velocity1 = 32;
		now_velocity2 = 32;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));
	state = IDLE

def M_BWD():
	global now_velocity1
	global now_velocity2
	global direction1
	global direction2
	global state
	if direction1 == 1:
		Device1.writereq(0xd,'544457650D0A') #BACK
		Device1.notify()
		direction1 = -1;
	if direction2 == 1:
		Device2.writereq(0xd,'544457650D0A') #BACK
		Device1.notify()	
		direction2 = -1;	
	now_velocity2 = 16;
	now_velocity1 = 16;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));
	state = IDLE

def M_ROTATE_LEFT():
	global now_velocity1
	global now_velocity2
	global direction1
	global direction2
	global state
	M_STOP()
	if direction1 == -1:
		Device1.writereq(0xd,'544443790D0A') #FRONT
		Device1.notify()
		direction1 = 1;
	if direction2 == 1:
		Device2.writereq(0xd,'544457650D0A') #BACK
		Device2.notify()
		direction2 = -1;
	now_velocity2 = 16;
	now_velocity1 = 16;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));
	state = IDLE
def M_ROTATE_RIGHT():
	global now_velocity1
	global now_velocity2
	global direction1
	global direction2
	global state
	M_STOP()
	if direction2 == -1:
		Device2.writereq(0xd,'544443790D0A') #FRONT
		Device2.notify()
		direction2 = 1;
	if direction1 == 1:
		Device1.writereq(0xd,'544457650D0A') #BACK
		Device1.notify()
		direction1 = -1;
	now_velocity2 = 16;
	now_velocity1 = 16;
	desired_speed1(int(now_velocity1));
	desired_speed2(int(now_velocity2));
	state = IDLE

def M_GEAR_UP():
	global state
	global GEAR
	if GEAR == 3:
		GEAR = 3;
	else:
		GEAR=GEAR+1;
	state = IDLE

def M_GEAR_DOWN():
	global state
	global GEAR
	if GEAR == 1:
		GEAR = 1;
	else:
		GEAR = GEAR-1;
	state = IDLE

prev_senddata2 = ""
prev_senddata1 = ""

def desired_speed2(desired):
	global prev_senddata2
	
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
	if senddata != prev_senddata2:	
		Device2.writereq(0xd,senddata)#Desired Speed
		Device2.notify()

def desired_speed1(desired):
	global prev_senddata1
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
	if senddata != prev_senddata1:	
		Device1.writereq(0xd,senddata)#Desired Speed
		Device1.notify()


keyboard.add_hotkey('w', M_FWD)
keyboard.add_hotkey('q', M_LEFT)
keyboard.add_hotkey('e', M_RIGHT)
keyboard.add_hotkey('a', M_LEFT2)
keyboard.add_hotkey('d', M_RIGHT2)
keyboard.add_hotkey('left', M_ROTATE_LEFT)
keyboard.add_hotkey('right', M_ROTATE_RIGHT)
keyboard.add_hotkey('up', M_GEAR_UP)
keyboard.add_hotkey('down', M_GEAR_DOWN)
keyboard.add_hotkey('s', M_BWD)
keyboard.add_hotkey('space', M_STOP)




def center_p(conners,depth_img):
	for conner in conners:
		for conner_p in conner:
			x,y = int(np.mean(conner_p[:,0])),int(np.mean(conner_p[:,1]))
			print(x,y)
			print(depth_img[y,x])

			#print(np.mean(conner[,0]))
def wheel_com():

	desired_speed1(10)
	desired_speed2(10)

	time.sleep(2)
	desired_speed1(0)
	desired_speed2(0)

	while 1:
		
		if state == STOP:
			M_STOP()
			state = STOP
		elif state == IDLE:
			M_IDLE()

		elif state == FWD:
			M_FWD();
			print("FWD")

		elif state == LEFT:
			print("LEFT")
			M_LEFT();
		elif state == RIGHT:
			print("RIGHT")
			M_RIGHT();



			
		print(state,direction1,direction2)
		time.sleep(0.5)
	

    #print("hhh")
def aruco_fun():
	cap = cv2.VideoCapture(0)
	pipe = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	profile = pipe.start(config)
	axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
	size_of_marker =  0.0145 # side lenght of the marker in meter
	while(True):
		time.sleep(0.5)
		frames = pipe.wait_for_frames()
		align_to = rs.stream.color
		align = rs.align(align_to)
		aligned_frames = align.process(frames)
		depth_frame = aligned_frames.get_depth_frame()
		color_frame = aligned_frames.get_color_frame()
		color_img = np.array(color_frame.get_data())
		color_img_temp = copy.deepcopy(color_img)
		depth_img = np.array(depth_frame.get_data())
		frame = color_img_temp 
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
		parameters =  aruco.DetectorParameters_create()
		corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
		frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
		cv2.imshow('frame',frame_markers)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

def main():
    t_wheel = threading.Thread(target=wheel_com)
    t_wheel.start()
    t_aruco = threading.Thread(target=aruco_fun)
    t_aruco.start()


#if __name__ =='__main__':
main()