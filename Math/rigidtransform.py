from __future__ import print_function
import math
from translation import Translation
from rotation import Rotation

class RigidTransform(object):
	
	global zero
	zero = 1E-9
	
	def __init__(self, translation_ = None, rotation_ = None):
		if translation_ == None:
			self.translation = Translation()
		else:
			self.translation = translation_
		if rotation_ == None:
			self.rotation = Rotation()		
		else:
			self.rotation = rotation_			
	
	def get_rotation(self):
		return self.rotation

	def get_translation(self):
		return self.translation

	def transform(self, other_transformation):
		return RigidTransform(self.translation.translate(other_transformation.get_translation().rotate(self.rotation)), self.rotation.rotate(other_transformation.get_rotation()))
	
	def inverse(self):
		return RigidTransform(self.translation.inverse().rotate(self.rotation.inverse()), self.rotation.inverse()) 

	'''
	ethaneade.com/lie_groups.pdf
	exponential map for rigid transformations
	this basically converts a twist (constant-curvature velocity) to a rigid transformation (pose)
	Twist: [[dx    ]
		[dy = 0] We don't move sideways
		[dtheta]]

	Rotation: [[cos(dtheta), -sin(dtheta)]
		   [sin(dtheta),  cos(dtheta)]]
	Translation: [[sin(dtheta)/dtheta,  -(1-cos(dtheta)/dtheta)]  * [[dx    ]
		      [(1-cos(dtheta)/dtheta,   sin(dtheta)/dtheta)]]    [dy = 0]]
	'''	
	@staticmethod
	def exp(twist):
		cos_theta = math.cos(twist.dtheta) 	
		sin_theta = math.sin(twist.dtheta)
		rotation = Rotation(cos_theta, sin_theta)
		#if theta is very small, use taylor series to approximate (we can't divide by zero) 
		if (math.fabs(twist.dtheta) < zero):
			sin_theta_over_theta = 1.0-math.pow(twist.dtheta, 2)/6.0 + math.pow(twist.dtheta, 4)/120.0	
			one_minus_cos_theta_over_theta = 1.0/2.0*twist.dtheta - math.pow(twist.dtheta, 3)/24.0 + math.pow(twist.dtheta, 5)/720.0
		else:
			sin_theta_over_theta = sin_theta/twist.dtheta
			one_minus_cos_theta_over_theta = (1.0-cos_theta)/twist.dtheta
		translation = Translation(sin_theta_over_theta*twist.dx, one_minus_cos_theta_over_theta*twist.dx)	
		return RigidTransform(translation, rotation)
	
	def intersection_(self, transform_a, transform_b):
		rotation_a = transform_a.get_rotation()
		rotation_b = transform_b.get_rotation()
		translation_a = transform_a.get_translation()
		translation_b = transform_b.get_translation()
		
		tan_b = rotation_b.get_tan()
		#???
		t = ((translation_a.get_x() - translation_b.get_x())*tan_b + translation_b.get_y() - translation_a.get_y())/(rotation_a.get_sin() - rotation_a.get_cos()*tan_b)
		return translation_a.translate(rotation_a.to_translation().scale(t))
	
	def intersection(self, other_transform):
		other_rot = other_transform.get_rotation()
		if (self.rotation.is_parallel(other_rot)):
			#should never reach here
			return Translation(float("inf"), float("inf"))
		if (math.fabs(self.rotation.get_cos()) < math.fabs(other_rot.get_cos())):
			return self.intersection_(self, other_transform)
		else:
			return self.intersection_(other_transform, self)	
	
	def print(self):
		print ("transform:")
		self.translation.print()
		self.rotation.print()

class Twist(object):
	
	def __init__(self, dx_ = None, dtheta_ = None):
		if dx_ == None:
			self.dx = 0
		else:
			self.dx = dx_
		if dtheta_ == None:
			self.dtheta = 0
		else:
			self.dtheta = dtheta_
	
	def scale(self, val):
		return Twist(self.dx*val, self.dtheta*val)
	
	def get_dx(self):
		return self.dx

	def get_dtheta(self):
		return self.dtheta
	
	def print(self):
		print("twist")
		print("dx: " + str(self.dx) + "\tdtheta: " + str(self.dtheta))
