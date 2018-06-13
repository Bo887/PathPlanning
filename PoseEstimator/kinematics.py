import sys
sys.path.append("../Math")
from rigidtransform import RigidTransform
from rigidtransform import Twist
from rotation import Rotation

track = 20

def forward_kinematics(left_delta, right_delta):
	delta_v = (right_delta-left_delta)
	delta_rotation = delta_v/track
	dx = (left_delta+right_delta)/2.0
	return Twist(dx, delta_rotation) 

def integrate_forward_kinematics(current_pose, current_velocity):
	return current_pose.transform(RigidTransform.exp(current_velocity)) 
