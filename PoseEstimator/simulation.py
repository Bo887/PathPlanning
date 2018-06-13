from __future__ import print_function
import sys
sys.path.append("../Math")
import math
from pose_estimator import PoseEstimator
from rigidtransform import RigidTransform
from rigidtransform import Twist
from translation import Translation
from rotation import Rotation

import matplotlib.pyplot as plt 

estimator = PoseEstimator()

#random values
#12 ft/s, 1 rad/s
twist = Twist(12.0, 1)
expected_end_pose = RigidTransform.exp(twist)
print("Expected Ending Pose: ")
expected_end_pose.print()

plt.ion()
axes = plt.gca()
axes.set_xlim([-20, 20])
axes.set_ylim([-20, 20])

def plot(): 
	iterations = 100
	l_enc = 0
	r_enc = 0
	track = 20 
	for i in range(iterations):
		#l_vel -> linear_vel + robot_track*angular_vel/2
		#r_vel -> linear_vel - robot_track*angular_vel/2
		l_vel = ((twist.get_dx() - track*twist.get_dtheta()/2.0))
		r_vel = ((twist.get_dx() + track*twist.get_dtheta()/2.0))
		#print("l_vel: " + str(l_vel) + "\tr_vel: " + str(r_vel))
		l_enc += l_vel*(1.0/iterations)
		r_enc += r_vel*(1.0/iterations)

		estimator.update(l_enc, r_enc)	
		pose = estimator.get_pose()	
		x = pose.get_translation().get_x()
		y = pose.get_translation().get_y()
		plt.scatter(x, y)
		plt.show()
		plt.pause(0.01)	
	while True:
		plt.pause(0.05)

if __name__ == "__main__":
	plot()
