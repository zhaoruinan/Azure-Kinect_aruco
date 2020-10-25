import open3d as o3d
import numpy as np
import cv2
import cv2.aruco as aruco

def center_p(conners,depth_img):
    for conner in conners:
        for conner_p in conner:
            x,y = int(np.mean(conner_p[:,0])),int(np.mean(conner_p[:,1]))
            #print(x,y)
            conner_p = np.array(conner_p,dtype=np.int16)
            d = []
            for p in conner_p:
                #print(p[0],p[1],depth[p[1],p[0]])
                d.append(depth[p[1],p[0]])
            print(d)
            #print(depth_img[conner_p])
            print(depth_img[y,x])

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
        color, depth = np.asarray(rgbd.color).astype(np.uint8), np.asarray(rgbd.depth).astype(np.uint16)
        return color, depth

config = o3d.io.AzureKinectSensorConfig()
v = ViewerWithCallback(config, 0, 1)

while True:
    color,depth_img = v.run()
    if color is None  or depth_img is None:
        continue
    frame = color
    depth = depth_img
    #print(color.shape,depth_img.shape)
    #depth_img = np.array(depth,dtype=float)/65535.0*255*5
    depth_img = np.logical_and(depth_img ,0x07FF)*255
    depth_img = np.array(depth_img,dtype=np.uint8)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    #print(corners,ids)
    if corners is not None:
        center_p(corners, depth)
    depth_img_jet = cv2.applyColorMap(depth_img, cv2.COLORMAP_JET)
    cv2.imshow('frame1',gray)
    cv2.imshow('frame',depth_img_jet)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
