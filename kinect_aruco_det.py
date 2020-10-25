import open3d as o3d
import numpy as np
import cv2
import cv2.aruco as aruco

def center_p(conners,depth_img):
    for conner in conners:
        for conner_p in conner:
            x,y = int(np.mean(conner_p[:,0])*576/720),int(np.mean(conner_p[:,1])/2)
            print(x,y)
            print(depth_img[x,y])

class ViewerWithCallback:
    def __init__(self, config, device, align_depth_to_color):
        self.flag_exit = False
        self.align_depth_to_color = align_depth_to_color

        self.sensor = o3d.io.AzureKinectSensor(config)
        if not self.sensor.connect(device):
            raise RuntimeError('Failed to connect to sensor')
    def escape_callback(self, vis):
        self.flag_exit = True
        return False
    def run(self):
        rgbd = self.sensor.capture_frame(self.align_depth_to_color)
        if rgbd is None:
            return None,None
        color, depth = np.asarray(rgbd.color).astype(np.uint8), np.asarray(rgbd.depth).astype(np.float32)
        return color, depth

config = o3d.io.AzureKinectSensorConfig()
v = ViewerWithCallback(config, 0, 1)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
size_of_marker =  0.0145 # side lenght of the marker in meter

while True:
    color,depth = v.run()
    if color is None  or depth is None:
        continue
    frame = color
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(corners,ids)
    rvecs,tvecs, trash = aruco.estimatePoseSingleMarkers(corners, size_of_marker , mtx, dist)

    imaxis = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    for i in range(len(tvecs)):
        imaxis = aruco.drawAxis(imaxis, mtx, dist, rvecs[i], tvecs[i], length_of_axis)

    #center_p(corners, depth)
    cv2.imshow('frame',imaxis)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
