from __future__ import print_function 
import unittest
import math

from translation import Translation
from rotation import Rotation
from rigidtransform import RigidTransform
from rigidtransform import Twist

class UnitTest(unittest.TestCase):
	
	def test_translation(self):
		#default constructor
		identity = Translation()
		self.assertEqual(identity.get_x(), 0.0)
		self.assertEqual(identity.get_y(), 0.0) 
		
		#normal constructor	
		t1 = Translation(10.0, 10.0)		
		self.assertEqual(t1.get_x(), 10.0)
		self.assertEqual(t1.get_y(), 10.0)
		
		#test tolerance
		t2 = Translation(1E-10, 1E-10)
		self.assertEqual(t2.get_x(), 0.0)
		self.assertEqual(t2.get_y(), 0.0)
		
		#test translating
		t3 = Translation(3.0,4.0)
		t4 = t3.translate(t1)
		self.assertAlmostEqual(t4.get_x(), 13.0)		
		self.assertAlmostEqual(t4.get_y(), 14.0)
		
		#test translating with negative values
		t5 = Translation(-9.0, -15.0)	
		t6 = t5.translate(t3)
		self.assertAlmostEqual(t6.get_x(), -6.0)
		self.assertAlmostEqual(t6.get_y(), -11.0)
		t7 = Translation(-3.0, -5.0)
		t8 = t7.translate(t5)
		self.assertAlmostEqual(t8.get_x(), -12.0)	
		self.assertAlmostEqual(t8.get_y(), -20.0)
	
		#test rotating
		r1 = Rotation()
		t1r1 = t1.rotate(r1)
		self.assertEquals(t1.get_x(), 10)
		self.assertEquals(t1.get_y(), 10)
		r2 = Rotation.from_degrees(45)
		t1r2 = t1.rotate(r2)
		self.assertAlmostEquals(t1r2.get_x(), 0)
		self.assertAlmostEquals(t1r2.get_y(), 10*math.sqrt(2.0))
		
		#test inverse
		t1i = t1.inverse()		
		self.assertEqual(t1i.get_x(), -10.0)
		self.assertEqual(t1i.get_y(), -10.0)
		t3i = t3.inverse()
		self.assertEqual(t3i.get_x(), -3.0)
		self.assertEqual(t3i.get_y(), -4.0)
		
		#test direction
		t1direction = t1.direction()
		self.assertAlmostEqual(t1direction.get_theta(), 45.0)
		t1idirection = t1i.direction()
		self.assertAlmostEqual(t1idirection.get_theta(), -135.0)	
	
		#test norm
		t1norm = t1.norm()
		self.assertAlmostEqual(t1norm, 10.0*math.sqrt(2.0))	
		t1inorm = t1i.norm()
		self.assertAlmostEqual(t1inorm, t1norm)
		t3norm = t3.norm()
		self.assertAlmostEqual(t3norm, 5.0)
		
		#test dot product
		t1t2dot = t1.dot(t2)	
		self.assertEqual(t1t2dot, 0.0)	
		t1t3dot = t1.dot(t3)
		self.assertAlmostEqual(t1t3dot, 70.0)
		t3t5dot = t3.dot(t5)
		self.assertAlmostEqual(t3t5dot, -87.0)
		t9 = Translation(3.0, -4.0)
		t3t9dot = t3.dot(t9)
		t9t3dot = t9.dot(t3)
		self.assertAlmostEqual(t3t9dot, t9t3dot)
		
		#test cross product
		t1t3cross = t1.cross(t3)
		t3t1cross = t3.cross(t1)
		self.assertGreater(t1t3cross, 0)
		self.assertLess(t3t1cross, 0)
		self.assertAlmostEqual(t1t3cross, -1.0*t3t1cross)	
		
		#test scale
		t1scaled = t1.scale(3.5)
		self.assertAlmostEqual(t1scaled.get_x(), 35.0)
		self.assertAlmostEqual(t1scaled.get_y(), 35.0)
		t3scaled = t3.scale(-2.0)	
		self.assertAlmostEqual(t3scaled.get_x(), -6.0)
		self.assertAlmostEqual(t3scaled.get_y(), -8.0)
	
		#test angle between two translations
		t10 = Translation(0, 10)
		t1t10angle = t1.get_angle(t10)	
		t10t1angle = t10.get_angle(t1)
		self.assertAlmostEqual(t1t10angle.get_theta(), 45.0)
		self.assertAlmostEqual(t1t10angle.get_theta(), t10t1angle.get_theta())
		t11 = Translation(0, 20)
		t10t11angle = t10.get_angle(t11)		
		self.assertEqual(t10t11angle.get_theta(), 0.0)
		t3t2angle = t3.get_angle(t2)	
		self.assertEqual(t3t2angle.get_theta(), 0.0)

		#test interpolation	
		t1t2half = t1.interpolate(t2, 0.5)
		self.assertAlmostEqual(t1t2half.get_x(), 5.0)
		self.assertAlmostEqual(t1t2half.get_y(), 5.0)	
		t11 = Translation(5.0, 5.0)
		t1t11half = t1.interpolate(t11, 0.5)
		self.assertAlmostEqual(t1t11half.get_x(), 7.5)	
		self.assertAlmostEqual(t1t11half.get_y(), 7.5)

	def test_rotation(self):
		
		#test constructor
		rot1 = Rotation()
		self.assertAlmostEqual(rot1.get_cos(), 1.0)
		self.assertAlmostEqual(rot1.get_sin(), 0.0)
		self.assertAlmostEqual(rot1.get_tan(), 0.0)
		
		rot2 = Rotation.from_degrees(90.0)
		self.assertAlmostEqual(rot2.get_tan(), float("inf"))
		rot3 = Rotation.from_radians(math.pi/2.0)
		self.assertAlmostEqual(rot2.get_theta(), rot3.get_theta())
		self.assertAlmostEqual(rot2.get_radians(), math.pi/2.0)

		rot4 = Rotation(1.0, 1.0, True)
		self.assertAlmostEqual(rot4.get_theta(), 45.0)
		self.assertAlmostEqual(rot4.get_tan(), 1.0)
		
		#test rotating
		rot5 = rot2.rotate(rot3)	
		self.assertAlmostEqual(rot5.get_theta(), 180.0)
		rot6 = Rotation.from_degrees(-27.0)	
		rot7 = rot6.rotate(rot2)
		self.assertAlmostEqual(rot7.get_theta(),63.0) 
		rot8 = rot2.rotate(rot6)
		self.assertAlmostEqual(rot8.get_theta(), 63.0)
		
		#test inverse
		rot2inv = rot2.inverse()	
		identity = Rotation()
		self.assertAlmostEqual(rot2inv.rotate(rot2).get_theta(), identity.get_theta())
		self.assertAlmostEqual(rot2inv.get_theta() + rot2.get_theta(), 0.0)

		#test is parallel
		self.assertTrue(rot2.is_parallel(rot2inv))
		self.assertFalse(rot2.is_parallel(rot6))
		
	def test_rigidtransform(self):
			
		#test constructor 
		pose1 = RigidTransform()
		self.assertEqual(pose1.get_translation().get_x(), 0.0)
		self.assertEqual(pose1.get_translation().get_y(), 0.0)
		self.assertEqual(pose1.get_rotation().get_theta(), 0.0)	
		pose2 = RigidTransform(Translation(10.0, 15.0), Rotation.from_degrees(45.0))
		self.assertEqual(pose2.get_translation().get_x(), 10.0)
		self.assertEqual(pose2.get_translation().get_y(), 15.0)
		self.assertEqual(pose2.get_rotation().get_theta(), 45.0)	

		#test transform
		pose3 = pose1.transform(pose2)	
		self.assertAlmostEqual(pose3.get_translation().get_x(), 10.0)
		self.assertAlmostEqual(pose3.get_translation().get_y(), 15.0)
		self.assertAlmostEqual(pose3.get_rotation().get_theta(), 45.0)
		pose4 = pose2.transform(pose1)
		self.assertAlmostEqual(pose4.get_translation().get_x(), 10.0)
		self.assertAlmostEqual(pose4.get_translation().get_y(), 15.0)
		self.assertAlmostEqual(pose4.get_rotation().get_theta(), 45.0)

		pose5 = RigidTransform(Translation(10.0, 10.0), Rotation.from_degrees(45.0))
		pose6 = pose5.transform(pose2)
		#used this link to verify: http://www.wolframalpha.com/widgets/view.jsp?id=bd71841fce4a834c804930bd48e7b6cf
		self.assertAlmostEqual(pose6.get_translation().get_x(), 10-(25/math.sqrt(2))+10*math.sqrt(2))
		self.assertAlmostEqual(pose6.get_translation().get_y(), 25/math.sqrt(2)+10*math.sqrt(2)-10*(-1+math.sqrt(2)))
		self.assertAlmostEqual(pose6.get_rotation().get_theta(), 90.0)
		
		pose7 = pose2.transform(pose5)	
		self.assertAlmostEqual(pose7.get_translation().get_x(), -25.0/math.sqrt(2) + 10*math.sqrt(2) + 5.0/2.0*(4+math.sqrt(2)))	
		self.assertAlmostEqual(pose7.get_translation().get_y(), 25.0/math.sqrt(2) + 10*math.sqrt(2) - 5.0/2.0*(-6+5*math.sqrt(2)))
		self.assertAlmostEqual(pose7.get_rotation().get_theta(), 90.0)
			
		#test inverse
		pose6inverse = pose6.inverse()
		pose8 = pose6.transform(pose6inverse)
		self.assertAlmostEqual(pose8.get_translation().get_x(), 0)
		self.assertAlmostEqual(pose8.get_translation().get_y(), 0)
		self.assertAlmostEqual(pose8.get_rotation().get_theta(), 0)

		#test intersection
		intersection_point = pose1.intersection(pose2)	
		self.assertAlmostEqual(intersection_point.get_x(), -5.0)
		self.assertAlmostEqual(intersection_point.get_y(), 0.0)
		
	def test_twist(self):		
		#test constructor
		twist1 = Twist()
		self.assertEqual(twist1.get_dx(), 0)
		self.assertEqual(twist1.get_dtheta(), 0)
			
		twist2 = Twist(10, 5)
		self.assertEqual(twist2.get_dx(), 10)	
		self.assertEqual(twist2.get_dtheta(), 5)
		
		#test scaling
		twist3 = twist2.scale(1.0/5.0)
		self.assertEqual(twist3.get_dx(), 2.0)
		self.assertEqual(twist3.get_dtheta(), 1.0)
		
		#test exp (generate pose from velocity)
		current_pose = RigidTransform.exp(Twist(1, 0))
		self.assertEqual(current_pose.get_translation().get_x(), 1.0)
		self.assertEqual(current_pose.get_translation().get_y(), 0.0)
		self.assertEqual(current_pose.get_rotation().get_theta(), 0.0)
		
if __name__ == '__main__':
			
	unittest.main()
