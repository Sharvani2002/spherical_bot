#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np
import sys, select, termios, tty
msg = '''
Control Micromouse using 
		w
	a 		d
		s

 and b for brake
'''

def getKey():
	tty.setraw(sys.stdin.fileno())
	rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
	if rlist:
		key = sys.stdin.read(1)
	else:
		key = ''
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key



if __name__ == '__main__':
	rospy.init_node('mm_teleop')
	settings = termios.tcgetattr(sys.stdin)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	
	# vmax = 0.4
	# amax = 0.1
	try:
		print(msg)
		while(1):
			cmd = Twist()
			key = getKey()
			speed_z = 0
			speed_x = 0.0
			if key=='w':
				speed_x += 0.4
			elif key=='b':
				speed_x = 0
				speed_z = 0
			elif key=='s':
				speed_x -= 0.4
			elif key=='d':
				speed_z -= 0.4
			elif key=='a':
				speed_z += 0.4
			elif (key == '\x03'):
				break
			# if speed_x>vmax:
			# 	speed_x = vmax
			# elif speed_x<-1*vmax:
			# 	speed_x = -1*vmax
			# if speed_z>amax:
			# 	speed_z = amax
			# elif speed_z<-1*amax:
			# 	speed_z = -1*amax
			cmd.linear.x = speed_x
			cmd.angular.z = speed_z
			pub.publish(cmd)
	except Exception as e:
		print(e)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)