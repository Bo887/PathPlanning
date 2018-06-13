from __future__ import print_function
import math
import rotation

class Translation(object):
	
	global zero
	zero = 1E-9

	def __init__(self, x_ = None, y_ = None):
		if x_ == None:
			self.x = 0	
		else:
			self.x = x_ if math.fabs(x_) > zero else 0
		if y_ == None:
			self.y = 0
		else:
			self.y = y_ if math.fabs(y_) > zero else 0
	
	@staticmethod
	def from_translations(translation_one, translation_two):
		return Translation(translation_two.get_x() - translation_one.get_x(), translation_two.get_y() - translation_one.get_y())
	
	def get_x(self):
		return self.x
	
	def get_y(self):
		return self.y

	def translate(self, other_translation):
		return Translation(self.x + other_translation.x, self.y + other_translation.y)

	'''
	[[x']  = [[cos, -sin]  * [[x]  = [[(cos)(x) + (-sin)(y)]
	 [y']]	  [sin,  cos]]    [y]]    [(sin)(x) +  (cos)(y)]]
	'''
	def rotate(self, other_rotation):
		return Translation(other_rotation.cos*self.x - other_rotation.sin*self.y, other_rotation.sin*self.x + other_rotation.cos*self.y)

	def inverse(self):
		return Translation(-self.x, -self.y)	
	
	#angle of translation with respect to positive horizontal axis`
	def direction(self):
		return rotation.Rotation(self.x, self.y, True)

	def norm(self):
		return math.hypot(self.x, self.y)		
	
	#dot product
	def dot(self, other_translation):
		return self.x*other_translation.x + other_translation.y*self.y

	#cross product (with z axis as 0)
	def cross(self, other_translation):
		return self.x*other_translation.y - self.y*other_translation.x

	def scale(self, val):
		return Translation(self.x*val, self.y*val)
	
	#angle between two translations
	def get_angle(self, other_translation):
		if self.norm() == 0 or other_translation.norm() == 0:
			return rotation.Rotation()
		cos = self.dot(other_translation)/(self.norm()*other_translation.norm())
		return rotation.Rotation.from_radians(math.acos(min(1.0, max(cos, -1.0))))	 
	
	def interpolate(self, other_translation, val):
		if val <= 0:
			return self
		elif val >= 1:
			return other_translation
		else:
			delta_x = other_translation.x - self.x	
			delta_y = other_translation.y - self.y
			return Translation(val*delta_x + self.x, val*delta_y + self.y)
		
	def print(self):
		print ("x: " + str(self.x) + "\ty: " + str(self.y))  
