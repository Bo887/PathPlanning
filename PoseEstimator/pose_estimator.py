from __future__ import print_function
import sys
sys.path.append("../Math")
from rigidtransform import RigidTransform
from rigidtransform import Twist
from translation import Translation
from rotation import Rotation
import kinematics

class PoseEstimator(object):
	
	def __init__(self):
		self.velocity = Twist(0,0)	
		self.pose = RigidTransform(Translation(0,0), Rotation.from_degrees(0)) 
		self.previous_pose = RigidTransform(Translation(0,0), Rotation.from_degrees(0)) 
		self.prev_left_pos = 0
		self.prev_right_pos = 0
	
	def reset(self):
		self.velocity = Twist(0,0)	
		self.pose = RigidTransform(Translation(0,0), Rotation.from_degrees(0)) 
		self.previous_pose = RigidTransform(Translation(0,0), Rotation.from_degrees(0)) 
		self.prev_left_pos = 0
		self.prev_right_pos = 0
	
	def get_pose(self):
		return self.pose
	
	def update(self, left_pos, right_pos):	
		delta_left_pos = left_pos-self.prev_left_pos
		delta_right_pos = right_pos-self.prev_right_pos
		#print(str(delta_left_pos) + "\t" + str(delta_right_pos))
		velocity = kinematics.forward_kinematics(delta_left_pos, delta_right_pos)
		#velocity.print()
		self.pose = kinematics.integrate_forward_kinematics(self.previous_pose, velocity) 
		self.prev_left_pos = left_pos
		self.prev_right_pos = right_pos
		self.previous_pose = self.pose	
