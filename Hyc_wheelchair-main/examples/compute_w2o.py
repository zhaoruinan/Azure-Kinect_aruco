import numpy as np
def get_xyz(conner,depth_img,cameraMatrix):
    camera_fx = cameraMatrix[0][0]
    camera_fy = cameraMatrix[1][1]
    camera_cx = cameraMatrix[0][2]
    camera_cy = cameraMatrix[1][2]
    conner_p = conner[0]
    n,m = int(np.mean(conner_p[:,0])),int(np.mean(conner_p[:,1]))
    z = depth_img[m,n]/1000.0
    x = (n - camera_cx) * z / camera_fx
    y = (m - camera_cy) * z / camera_fy
    return np.array([x,y,z])
def center_p(conners,depth_img,cameraMatrix):
    print(cameraMatrix)
    camera_fx = cameraMatrix[0][0]
    camera_fy = cameraMatrix[1][1]
    camera_cx = cameraMatrix[0][2]
    camera_cy = cameraMatrix[1][2]
    #print(fx,fy,cx,cy)
    print("conners",conners)
    for conner in conners:
        print("conner",conner)
        for conner_p in conner:
            print("conner_p",conner_p)
            n,m = int(np.mean(conner_p[:,0])),int(np.mean(conner_p[:,1]))
            print(n,m)
            print(depth_img[m,n])
            z = depth_img[m,n]
            x = (n - camera_cx) * z / camera_fx
            y = (m - camera_cy) * z / camera_fy
            print(x,y,z)

def compute_w2o(wheel_chair_rotation_vectors,wheel_chair_translation_vectors,obj_rotation_vectors,obj_translation_vectors):
    c2w = np.c_[wheel_chair_rotation_vectors,wheel_chair_translation_vectors[0]]
    temp = np.array([0,0,0,1])
    c2w = np.r_[c2w, [temp]]
    #w2c = np.linalg.inv(c2w)
    w2c = np.c_[wheel_chair_rotation_vectors.T,-wheel_chair_rotation_vectors.T.dot(wheel_chair_translation_vectors[0])]
    w2c = np.r_[w2c, [temp]]
    c2o = np.c_[obj_rotation_vectors,obj_translation_vectors[0]]
    c2o = np.r_[c2o, [temp]]                    
    w2o = w2c.dot(c2o)
    #p = w2o[:,3][:3]
    p =obj_translation_vectors[0] - wheel_chair_translation_vectors[0]
    #p = 0
    return p
