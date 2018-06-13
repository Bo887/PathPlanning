from path import Path
from generator import Generator
from generator import Waypoint
generator = Generator()
waypoints = []
'''
waypoints.append(Waypoint(50.0,50.0,0.0))
waypoints.append(Waypoint(160.0,50.0,60.0))
waypoints.append(Waypoint(260.0,140.0,0.0))
'''
waypoints.append(Waypoint(0.0,0.0,0.0))
waypoints.append(Waypoint(0.0, 10.0, 5.0))
waypoints.append(Waypoint(10.0, 10.0, 0.0))
#another path
'''
waypoints.append(Waypoint(50.0, 50.0, 0.0))
waypoints.append(Waypoint(160.0, 50.0, 50.0))
waypoints.append(Waypoint(220.0, 140.0, 50.0))
waypoints.append(Waypoint(340.0, 200.0, 0.0))
'''
path = generator.generate(waypoints)
path.plot()
