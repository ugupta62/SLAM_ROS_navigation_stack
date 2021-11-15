#!/usr/bin/env python
import rospy
import numpy as np
import sys
from geometry_msgs.msg import PoseStamped, Twist

pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size = 1)

#### global varaibales ####
checkpoint = 0
cmd_vel = 0
cmd_omega = 0
'''
Mahdi Ghanei and Ujjwal Gupta
'''
waypoints = rospy.get_param("waypoint")
 
def callback(data):
	
	global cmd_vel, cmd_omega, checkpoint
	
	cmd_vel = data.linear.x 
	cmd_omega = data.angular.z
	
	pose = waypoints[checkpoint]
	position = pose[0:3]
	orientation = pose[3:]

	# publish the waypoint to /move_base_simple/goal topic
	pose = PoseStamped()
	pose.position.x = position[0]
	pose.position.y = position[1]
	pose.orientation.x = orientation[0]
	pose.orientation.y = orientation[1]
	pose.orientation.z = orientation[2]
	pose.orientation.w = orientation[3]
	pub.publish(pose)
	
	# check if reached the checkpoint
	if cmd_vel == 0 and cmd_omega == 0:
		checkpoint = checkpoint + 1
		print('\n\n\n****************************************checkpoint {checkpoint} reached!')
		if checkpoint == 3:
			sleep(100.0)
		else:
			sleep(2.0)
	

     	
def nav_waypoint():  #obstacle range
     	
	rospy.init_node('navigate_to_goal_point', anonymous=True)
	zero_vel =  int(sys.argv[1])

	if zero_vel>0:
		oldtime = time()
		while (time() - oldtime) < 5:
			pubRobot(0,0)
		print('published zero')
	
	else:
		rospy.Subscriber('/cmd_vel', Twist, callback,  queue_size = 1)
   	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
 
if __name__ == '__main__':
	nav_waypoint()
	

	# if rospy.is_shutdown():
	# 	pub.publish(stop)
