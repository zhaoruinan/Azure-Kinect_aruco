import numpy as np
import cv2
import cv2.aruco as aruco
#from aruco_lib import *
import pyrealsense2 as rs
import copy
import threading
from datetime import datetime
import sys, time
import keyboard
from threading import Timer
from bledevice import scanble, BLEDevice
import socket
import struct
import random
from compute_w2o import compute_w2o,center_p,get_xyz
from datetime import datetime
from ctypes import *
SIZE_DATA_TCP_MAX  = 200
class Data(Union):
    _fields_ = [("byte", c_ubyte * SIZE_DATA_TCP_MAX),("int7Arr", c_int * 7),("float63dArr", c_float * 63)]

write_buffer = (c_char* 1024)()  

#HOST = '192.168.50.4'  # The server's hostname or IP address
HOST = "127.0.0.1"
PORT = 9911		# The port used by the server
ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)
board = aruco.GridBoard_create(
		markersX=1,
		markersY=1,
		markerLength=0.06,
		markerSeparation=0.01,
		dictionary=ARUCO_DICT)


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
	start = datetime.now()
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
	end = datetime.now()
	exec_time = end - start
	print("blueteeth time",exec_time,exec_time.total_seconds())

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




def tcp_init():
	global client, send_data
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (HOST, PORT)
	client.connect(server_address)
	send_data = Data()
def tcp_com():

	#'''
	global client
	global send_data
	start = datetime.now()
	send_data.int7Arr[0]=random.randrange(1,100)
	memmove( write_buffer, send_data.byte,1024)

	send_data.float63dArr[5]=random.uniform(0, 1)
	#print(send_data.float63dArr[5])
	send_data.int7Arr[0]=random.randrange(1,100)
	client.sendall(write_buffer)
	end = datetime.now()
	#print(write_buffer[:50])
	#res = [ord(sub) for sub in  write_buffer[:50]] 
	#print(res)
    #send_data.int7Arr[1]=100
    #send_data.double6dArr[0]=3.3
    #memmove( write_buffer, send_data.byte,1024)
    #client.sendall(write_buffer)
    #end = datetime.now()
    #exec_time = end - start
    #print(send_data.double6dArr[0])
    #print(end)
    #print(exec_time,exec_time.total_seconds())
    #time.sleep(0.2-exec_time.total_seconds())
    #read_buffer = s.recv(1024)
    #res = [ord(sub) for sub in  write_buffer[:50]] 
    #print(res)
	#'''



def wheel_com_init():
	global Device1, Device2
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


	desired_speed1(10)
	desired_speed2(10)

	time.sleep(2)
	desired_speed1(0)
	desired_speed2(0)
	global state
	state = STOP


def wheel_com():

	global time_stamp1
	time_stamp1=datetime.now()
	global time_stamp2
	time_stamp2=datetime.now()
	#state = STOP
	global state

	if 1:
	#while 1:
		
		time_stamp1 = datetime.now()
		print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
		print("wheel control")
		exectime1 = time_stamp1 - time_stamp2
		print(exectime1.total_seconds())
		
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



		time_stamp2 = time_stamp1
		print(state,direction1,direction2)
		#time.sleep(0.5)

	

    #print("hhh")
def aruco_init():
	global pipe, cameraMatrix, distCoeffs, find_wheel_chair,depth_intrinsics
	cap = cv2.VideoCapture(0)
	pipe = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	profile = pipe.start(config)
	cameraMatrix = np.load('mtx.npy')
	color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))
	color_intrinsics = color_profile.get_intrinsics()
	depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
	depth_intrinsics = depth_profile.get_intrinsics()
	print(color_intrinsics)
	distCoeffs = np.load('dist.npy')
	find_wheel_chair = 0
def process_data(ids,rotation_mat):
	global send_data
	for i in range(3):
		for j in range(3):
			index = 10+ids*9+i*3+j
			#send_data.double6dArr[index] = rotation_mat[i,j]

	#send_data.double6dArr[10]=rotation_mat(0, 1)
def aruco_fun():
	global pipe, cameraMatrix, distCoeffs, depth_intrinsics
	axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
	if True:
		
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
		#print(corners,ids)
		#center_p(corners, depth_img,cameraMatrix)
		#if False:
		if ids is not None and len(ids) > 0:
			global wheel_chair_translation_vectors, find_wheel_chair
			#print("len",len(ids[0]))
			num = int(len(ids))
			for id_obj in range(num):

				if ids[id_obj] == 6:
					find_wheel_chair = 1
					wheel_chair_translation_vectors = get_xyz(corners[id_obj], depth_img,cameraMatrix,depth_intrinsics)
				elif ids[id_obj]!=6:
					if find_wheel_chair == 0:
						continue
					obj_translation_vectors = get_xyz(corners[id_obj], depth_img,cameraMatrix,depth_intrinsics)
					p = obj_translation_vectors - wheel_chair_translation_vectors
					print(ids[id_obj]," ","postion vetor is",p)
					#process_data(ids[id_obj],p)
		gray = aruco.drawDetectedMarkers(gray, corners)
		cv2.imshow('frame',gray)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			#break
	if False:
	#while(True):
		frames = pipe.wait_for_frames()
		
		color_frame = frames.get_color_frame()
		# Convert images to numpy arrays
		color_image = np.asanyarray(color_frame.get_data())
		gray = cv2.cvtColor(color_image.copy(), cv2.COLOR_RGB2GRAY)
		corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, ARUCO_DICT, parameters=ARUCO_PARAMETERS)
		corners, ids, rejectedImgPoints, recoveredIds = aruco.refineDetectedMarkers(
				image = gray,
				board = board,
				detectedCorners = corners,
				detectedIds = ids,
				rejectedCorners = rejectedImgPoints,
				cameraMatrix = cameraMatrix,
				distCoeffs = distCoeffs)
		ProjectImage = color_image.copy()
		ProjectImage = aruco.drawDetectedMarkers(ProjectImage, corners, borderColor=(0, 0, 255))
		print(ids)
		if ids is not None and len(ids) > 0:
			# Estimate the posture per each Aruco marker
			rotation_vectors, translation_vectors, _objPoints = aruco.estimatePoseSingleMarkers(corners, 1, cameraMatrix, distCoeffs)
			#global wheel_chair_rotation_vectors,  wheel_chair_translation_vectors, find_wheel_chair ,w2c
			print("len",len(ids[0]))
			num = int(len(ids))
			for id_obj in range(num):

				if ids[id_obj] == 6:
					find_wheel_chair = 1
					wheel_chair_rotation_vectors =cv2.Rodrigues( rotation_vectors[id_obj][0])[0]
					wheel_chair_translation_vectors = rotation_vectors[id_obj]
					c2w = np.c_[wheel_chair_rotation_vectors,wheel_chair_translation_vectors[0]]
					temp = np.array([0,0,0,1])
					c2w = np.r_[c2w, [temp]]
					#w2c = np.linalg.inv(c2w) 
					w2c = np.c_[wheel_chair_rotation_vectors.T,-wheel_chair_rotation_vectors.T.dot(wheel_chair_translation_vectors[0])]
					w2c = np.r_[w2c, [temp]]
				elif ids[id_obj]!=6:
					if find_wheel_chair == 0:
						continue
					obj_rotation_vectors =cv2.Rodrigues( rotation_vectors[id_obj][0])[0]
					obj_translation_vectors = rotation_vectors[id_obj]
					c2o = np.c_[obj_rotation_vectors,obj_translation_vectors[0]]

					temp = np.array([0,0,0,1])
					c2o = np.r_[c2o, [temp]]					
					w2o = w2c.dot(c2o)
					#p = w2o[:,3][:3]
					p = compute_w2o(wheel_chair_rotation_vectors,wheel_chair_translation_vectors,obj_rotation_vectors,obj_translation_vectors)
					
					print(ids[id_obj]," ","postion vetor is",p)
					#process_data(ids[id_obj],p)
				
			ids = 1

			for rvec in rotation_vectors:
				rotation_mat = cv2.Rodrigues(rvec[0])[0]
				ids = ids+1
				

			for rvec, tvec in zip(rotation_vectors, translation_vectors):
				if len(sys.argv) == 2 and sys.argv[1] == 'cube':
					try:
						imgpts, jac = cv2.projectPoints(axis, rvec, tvec, cameraMatrix, distCoeffs)
						ProjectImage = drawCube(ProjectImage, corners, imgpts)
					except:
						continue
				else:    
					ProjectImage = aruco.drawAxis(ProjectImage, cameraMatrix, distCoeffs, rvec, tvec, 1)
		cv2.imshow('ProjectImage', ProjectImage)
		#frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
		#cv2.imshow('frame',frame_markers)
		#end = datetime.now()
		#exec_time = end - start
		#print("aruco control")
		#print(exec_time,exec_time.total_seconds())
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			#break
class RepeatingTimer(Timer): 
	def run(self):
		while not self.finished.is_set():
			self.function(*self.args, **self.kwargs)
			self.finished.wait(self.interval)
def main():

	#tcp_init()
	#t_tcp = RepeatingTimer(0.03, tcp_com)
	#t_tcp.start()

	aruco_init()
	#wheel_com_init()
	t_aruco = RepeatingTimer(0.2, aruco_fun)
	t_aruco.start()
	#t_wheel = RepeatingTimer(0.125, wheel_com)
	#t_wheel.start()
    #t_wheel = threading.Thread(target=wheel_com)
    #t_wheel.start()
    #t_aruco = threading.Thread(target=aruco_fun)
    #t_aruco.start()

#if __name__ =='__main__':
main()