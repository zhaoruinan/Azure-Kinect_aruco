import numpy as np
import cv2
import cv2.aruco as aruco
#from aruco_lib import *
import time
import pyrealsense2 as rs
import copy
import threading



def center_p(conners,depth_img):
	for conner in conners:
		for conner_p in conner:
			x,y = int(np.mean(conner_p[:,0])),int(np.mean(conner_p[:,1]))
			print(x,y)
			print(depth_img[y,x])

			#print(np.mean(conner[,0]))

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
    t_aruco = threading.Thread(target=aruco_fun)
    t_aruco.start()


#if __name__ =='__main__':
main()