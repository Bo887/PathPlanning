from __future__ import print_function
import sys
sys.path.append("../Math")
from translation import Translation
from rotation import Rotation
from rigidtransform import RigidTransform
from segment import Segment
from path import Path

class Waypoint(object):
	
	def __init__(self, x_, y_, radius_):
		self.position = Translation(x_, y_)
		self.radius = radius_
	
	def get_position(self):
		return self.position
	
	def get_radius(self):
		return self.radius

class Line(object):
	
	def __init__(self, waypoint_one, waypoint_two):
		self.slope = Translation.from_translations(waypoint_one.get_position(), waypoint_two.get_position())
		self.start = waypoint_one.get_position().translate(self.slope.scale(waypoint_one.get_radius()/self.slope.norm()))
		self.end = waypoint_two.get_position().translate(self.slope.scale(-1.0*(waypoint_two.get_radius()/self.slope.norm())))

	
	def add_to_path(self, path):
		length = Translation.from_translations(self.start, self.end).norm()
		if length > 1E-9:
			path.add_segment(Segment(self.start.get_x(), self.start.get_y(), self.end.get_x(), self.end.get_y()))

	def get_start(self):
		return self.start
	
	def get_end(self):
		return self.end

	def get_slope(self):
		return self.slope

class Arc(object):

	def __init__(self, line_one_, line_two_):
		self.line_one = line_one_
		self.line_two = line_two_
		normal_line_one = RigidTransform(self.line_one.end, Rotation.from_translation(self.line_one.slope, True).normal())	
		normal_line_two = RigidTransform(self.line_two.start, Rotation.from_translation(self.line_two.slope, True).normal())
		self.center = normal_line_one.intersection(normal_line_two)	
		center_to_end_dist = Translation.from_translations(self.center, self.line_one.end).norm()
		start_to_center_dist = Translation.from_translations(self.center, self.line_two.start).norm() 
		if (center_to_end_dist-start_to_center_dist > 1E-9):
			#should never enter here
			print("ERROR, CENTER OF ARC IS CALCULATED INCORRECTLY")
			self.radius = 7777 
		else:
			self.radius = center_to_end_dist
	
	@staticmethod
	def from_points(wp_one, wp_two, wp_three):
		return Arc(Line(wp_one, wp_two), Line(wp_two, wp_three))

	def add_to_path(self, path):
		self.line_one.add_to_path(path)
		if (self.radius > 1E-9 and self.radius < 1E9):
			path.add_segment(Segment(self.line_one.get_end().get_x(), self.line_one.get_end().get_y(), self.line_two.get_start().get_x(), self.line_two.get_start().get_y(), self.center.get_x(), self.center.get_y()))

	def get_line_one(self):
		return self.line_one
	
	def get_line_two(self):
		return self.line_two
	
	def get_center(self):	
		return self.center
	
	def get_radius(self):
		return self.radius

class Generator(object):
	
	@staticmethod
	def generate(waypoints):
		path = Path()	
		for i in range(0, len(waypoints)-2):	
			Arc.from_points(waypoints[i], waypoints[i+1], waypoints[i+2]).add_to_path(path)	
		Line(waypoints[len(waypoints)-2], waypoints[len(waypoints)-1]).add_to_path(path)
		return path

