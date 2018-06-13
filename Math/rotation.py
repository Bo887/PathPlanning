from __future__ import print_function
import math

import translation
'''
implements a 2d rotation matrix
	[[cos(theta), -sin(theta)]
	 [sin(theta),  cos(theta)]]
'''
class Rotation(object):

	#cutoff for rounding errors
	global zero
	zero = 1E-9	
	
	def __init__(self, cos_ = None, sin_ = None, normalize_ = None):
		if cos_ == None:
			self.cos = 1
		else: 	
			self.cos = cos_ if math.fabs(cos_) > zero else 0
		if sin_ == None:
			self.sin = 0
		else:
			self.sin = sin_ if math.fabs(sin_) > zero else 0
		#rescale sin and cos values to overcome rounding errors 
		if normalize_:
			magnitude = math.hypot(self.cos, self.sin)	
			if magnitude > zero:
				self.sin/=magnitude
				self.cos/=magnitude
			else:
				self.sin = 0
				self.cos = 1
		self.theta_rad = math.atan2(self.sin, self.cos)
		self.theta = self.theta_rad*180.0/math.pi
	
	@staticmethod
	def from_radians(rad):
		return Rotation(math.cos(rad), math.sin(rad))
	
	@staticmethod
	def from_degrees(degrees):
		radians = degrees/180.0*math.pi 
		return Rotation.from_radians(radians)

	@staticmethod
	def from_translation(translation, normalize):
		return Rotation(translation.get_x(), translation.get_y(), normalize)

	def get_cos(self):
		return self.cos
	
	def get_sin(self):
		return self.sin
	
	def get_tan(self):
		if (math.fabs(self.cos) < 1E-9):
			return float("inf") if self.sin > 0 else -float("inf") 
		return self.sin/self.cos

	#in degrees
	def get_theta(self):
		return self.theta
	
	def get_radians(self):
		return self.theta_rad
	
	def normal(self):
		return Rotation(-self.sin, self.cos)
		
	'''
	multiply the two rotation matrices together
	[[cos, -sin]  * [[cos', -sin']  = [[(cos)*(cos')+(-sin)*(sin'), (cos)*(-sin')+(-sin')*(cos)]
	 [sin,  cos]]    [sin',  cos']]    [(sin)*(cos')+(cos)*(sin'),  (sin)*(-sin')+(cos)*(cos') ]] 
	'''
	def rotate(self, other_rot):
		return Rotation(self.cos*other_rot.cos - self.sin*other_rot.sin, self.sin*other_rot.cos + self.cos*other_rot.sin,True)	

	'''
	Since this is an orthagonal matrix, the inverse is the same as the transpose 
	Calculating the transpose instead of the inverse is much more cost efficient	
	[[cos, -sin] T  =  [[ cos, sin]
	 [sin,  cos]]  	    [-sin, cos]]
	cos stays the same, sin is multiplied by -1 
	'''
	def inverse(self):
		return Rotation(self.cos, -self.sin)	

	def to_translation(self):
		return translation.Translation(self.cos, self.sin)
	
	#two rotations are parallel when the cross product of their translations are 0
	def is_parallel(self, other_rotation):
		return math.fabs(self.to_translation().cross(other_rotation.to_translation()))<zero 

	def print(self):
		print ("theta: " + str(self.theta) + "\tcos: " + str(self.cos) + "\tsin: " + str(self.sin))
