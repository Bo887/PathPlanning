from __future__ import print_function
import unittest
import math
import sys
sys.path.append("../Math/")

from generator import Waypoint
from generator import Line
from generator import Arc
from generator import Generator
from segment import Type
from translation import Translation

class UnitTest(unittest.TestCase):

	def test_waypoint(self):
		wp1 = Waypoint(0, 0, 0)
		self.assertEqual(wp1.get_position().get_x(), 0)
		self.assertEqual(wp1.get_position().get_y(), 0)
		self.assertEqual(wp1.get_radius(), 0)
	
	def test_line(self):
		wp1 = Waypoint(1, 3, 0)
		wp2 = Waypoint(4, 10, 0)
		line1 = Line(wp1, wp2)
		self.assertEqual(line1.get_slope().get_x(), 3)
		self.assertEqual(line1.get_slope().get_y(), 7)
		self.assertEqual(line1.get_start().get_x(), 1)
		self.assertEqual(line1.get_start().get_y(), 3)
		self.assertEqual(line1.get_end().get_x(), 4)
		self.assertEqual(line1.get_end().get_y(), 10)
		wp3 = Waypoint(0, 0, 0)
		wp4 = Waypoint(0, 10, 1)
		line2 = Line(wp3, wp4)
		self.assertEqual(line2.get_slope().get_x(), 0)
		self.assertEqual(line2.get_slope().get_y(), 10)
		self.assertEqual(line2.get_start().get_x(), 0)
		self.assertEqual(line2.get_start().get_y(), 0)
		self.assertEqual(line2.get_end().get_x(), 0)
		#the end of this line is 9 due to the 1 unit radius
		self.assertEqual(line2.get_end().get_y(), 9)

	def test_arc(self):
		wp0 = Waypoint(0, 0, 0)
		wp1 = Waypoint(0, 10, 5)
		wp2 = Waypoint(10, 10, 0)
		line1 = Line(wp0, wp1)	
		line2 = Line(wp1, wp2)
		arc1 = Arc(line1, line2)
		self.assertEqual(arc1.get_line_one().get_start().get_x(), 0)
		self.assertEqual(arc1.get_line_one().get_start().get_y(), 0)
		#end of first line adjusted for arc
		self.assertEqual(arc1.get_line_one().get_end().get_x(), 0)
		self.assertEqual(arc1.get_line_one().get_end().get_y(), 5)
		#start of second line adjusted for arc
		self.assertEqual(arc1.get_line_two().get_start().get_x(), 5)
		self.assertEqual(arc1.get_line_two().get_start().get_y(), 10)
		self.assertEqual(arc1.get_line_two().get_end().get_x(), 10)
		self.assertEqual(arc1.get_line_two().get_end().get_y(), 10)
			
		self.assertEqual(arc1.get_radius(), 5.0)
		self.assertEqual(arc1.get_center().get_x(), 5)
		self.assertEqual(arc1.get_center().get_y(), 5)

	def test_generate_path(self):
		generator = Generator()	
		waypoints = []
		waypoints.append(Waypoint(0.0,0.0,0.0))
		waypoints.append(Waypoint(0.0,10.0,5.0))
		waypoints.append(Waypoint(10.0,10.0,0.0))
		path = generator.generate(waypoints)
		num_segs = path.get_num_segments()	
		self.assertEqual(num_segs, 3)
		segments = path.get_segments() 
		#1st segment:	
		#Line: (0,0) -> (0,5)
		self.assertEqual(segments[0].get_start_point().get_x(), 0.0)
		self.assertEqual(segments[0].get_start_point().get_y(), 0.0)
		self.assertEqual(segments[0].get_end_point().get_x(), 0.0)
		self.assertEqual(segments[0].get_end_point().get_y(), 5.0)
		self.assertEqual(segments[0].get_type(), Type.LINE)
		self.assertEqual(segments[0].get_center(), None)
		self.assertEqual(segments[0].get_radius(), None)
		#2nd segment:
		#Arc: (0,5) -> (5,10), Center = (5,5), Radius = 5
		self.assertEqual(segments[1].get_start_point().get_x(), 0.0)
		self.assertEqual(segments[1].get_start_point().get_y(), 5.0)
		self.assertEqual(segments[1].get_end_point().get_x(), 5.0)
		self.assertEqual(segments[1].get_end_point().get_y(), 10.0)
		self.assertEqual(segments[1].get_type(), Type.ARC)
		self.assertEqual(segments[1].get_center().get_x(), 5.0)
		self.assertEqual(segments[1].get_center().get_y(), 5.0)
		self.assertEqual(segments[1].get_radius(), 5.0)
		#3rd segment:
		#Line: (5, 10) -> (10, 10)
		self.assertEqual(segments[2].get_start_point().get_x(), 5.0)
		self.assertEqual(segments[2].get_start_point().get_y(), 10.0)
		self.assertEqual(segments[2].get_end_point().get_x(), 10.0)
		self.assertEqual(segments[2].get_end_point().get_y(), 10.0)
		self.assertEqual(segments[2].get_type(), Type.LINE)
		self.assertEqual(segments[2].get_center(), None)
		self.assertEqual(segments[2].get_radius(), None)

if __name__ == "__main__":	
	unittest.main()
