from segment import Type

class Path(object):

	def __init__(self):
		self.segments = []

	def add_segment(self, segment):
		self.segments.append(segment)
	
	def get_num_segments(self):
		return len(self.segments)

	def get_segments(self):
		return self.segments
	
	def plot(self):
		import matplotlib.patches as mpatches
		import matplotlib.pyplot as plt
		import matplotlib.patches as patch	
		fig, ax = plt.subplots(1, 1)
		max_x = -1000000
		max_y = -1000000
		min_x = 1000000
		min_y = 1000000
		for i in range(0, self.get_num_segments()):
			seg = self.segments[i]
			start = seg.get_start_point()
			end = seg.get_end_point()
			max_x = max(start.get_x(), max(end.get_x(), max_x))
			min_x = min(start.get_x(), min(end.get_x(), min_x))
			max_y = max(start.get_y(), max(end.get_y(), max_y))
			min_y = min(start.get_y(), min(end.get_y(), min_y))
			if (seg.get_type() == Type.LINE):
				x1 = [start.get_x(), end.get_x()]	
				x2 = [start.get_y(), end.get_y()]
				plt.plot(x1, x2)
			else:
				center = seg.get_center()
				radius = seg.get_radius()
				start_angle = self.segments[i-1].get_slope().direction().get_theta()
				end_angle = self.segments[i+1].get_slope().direction().get_theta()
				#arc = patch.Arc([center.get_x(), center.get_y()], radius*2, radius*2, angle=0, theta1=start_angle-90.0, theta2=end_angle-90.0)
				arc = patch.Arc([center.get_x(), center.get_y()], radius*2, radius*2)
				ax.add_patch(arc)
				
		plt.axis("scaled")
		offset_x = (max_x-min_x)/4.0
		plt.xlim(min_x-offset_x, max_x+offset_x)
		offset_y = (max_y-min_y)/4.0
		plt.ylim(min_y-offset_y, max_y+offset_y)
		plt.show()
