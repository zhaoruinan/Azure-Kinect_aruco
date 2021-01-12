import numpy as np
import cv2
import cv2.aruco as aruco
#from aruco_lib import *
import time
import pyrealsense2 as rs
import copy
def center_p(conners,depth_img):
	for conner in conners:
		for conner_p in conner:
			x,y = int(np.mean(conner_p[:,0])),int(np.mean(conner_p[:,1]))
			print(x,y)
			print(depth_img[y,x])

			#print(np.mean(conner[,0]))
def main():
	cap = cv2.VideoCapture(0)
	pipe = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	profile = pipe.start(config)
	while(True):
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
		print(corners,ids)
		center_p(corners, depth_img)
		gray = aruco.drawDetectedMarkers(gray, corners)
		cv2.imshow('frame',gray)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
#if __name__ =='__main__':
main()