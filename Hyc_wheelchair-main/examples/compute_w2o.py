import numpy as np
def center_p(conners,depth_img):
	for conner in conners:
		for conner_p in conner:
			x,y = int(np.mean(conner_p[:,0])),int(np.mean(conner_p[:,1]))
			print(x,y)
			print(depth_img[y,x])
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
