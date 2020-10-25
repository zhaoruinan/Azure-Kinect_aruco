from pyk4a import PyK4A
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
			x,y = int(np.mean(conner_p[:,0])*576/720),int(np.mean(conner_p[:,1])/2)
			print(x,y)
			print(depth_img[x,y]*1000)

			#print(np.mean(conner[,0]))
def main():
	k4a = PyK4A()
	k4a.start()
	img_num =1
	while(True):
		capture = k4a.get_capture()
		img_color = capture.color
		depth_img = capture.depth
		print(depth_img.shape)
		print(img_color.shape)
		frame = img_color[:, :, 2::-1]
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
		parameters =  aruco.DetectorParameters_create()
		corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
		print(corners,ids)
		depth_img = depth_img /10000
		center_p(corners, depth_img)
		gray = aruco.drawDetectedMarkers(gray, corners)
		cv2.imshow('frame',depth_img /10000)
		#cv2.imshow('frame2',depth_img/8.0)
		if cv2.waitKey(1) & 0xFF == ord('s'):
			cv2.imwrite("cam_cal_img/"+str(img_num) + "cal.png", gray)
			img_num += 1
		if cv2.waitKey(10) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
#if __name__ =='__main__':
main()