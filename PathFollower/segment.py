from __future__ import print_function
import sys
sys.path.append("../Math")
from enum import Enum
from translation import Translation
	
class Type(Enum):
	LINE = 0
	ARC = 1

class Segment(object):

	def __init__(self, start_x, start_y, end_x, end_y, center_x = None, center_y = None):
		self.start = Translation(start_x, start_y)
		self.end = Translation(end_x, end_y)
		if center_x == None and center_y == None:
			self.slope = Translation.from_translations(self.start, self.end)
			self.segment_type = Type.LINE
		else:
			self.segment_type = Type.ARC
			self.center = Translation(center_x, center_y)
			center_to_start = Translation.from_translations(self.center, self.start)
			center_to_end = Translation.from_translations(self.center, self.end)
			if (center_to_start.norm()-center_to_end.norm() < 1E-9):
				self.radius = center_to_start.norm()
			else: 
				self.radius = -3256
	
	def get_type(self):
		return self.segment_type
	
	def get_start_point(self):
		return self.start
		
	def get_end_point(self):
		return self.end
	
	def get_slope(self):
		if (self.segment_type == Type.LINE):
			return self.slope
		return None
	
	def get_center(self):
		if (self.segment_type == Type.ARC):
			return self.center
		return None
	
	def get_radius(self):
		if (self.segment_type == Type.ARC):
			return self.radius
		return None

	def get_closest_point_on_segment(self, robot_pose):
		return

	def get_lookahead_point(self, closest_point, lookahead_distance):
		return
