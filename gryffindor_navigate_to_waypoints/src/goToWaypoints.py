#!/usr/bin/env python
import rospy
import numpy as np
import sys
from time import time, sleep
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, Twist
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import GoalStatusArray

pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size = 1)
pub_vel = rospy.Publisher("/cmd_vel", Twist, queue_size = 5)

#### global varaibales ####
checkpoint = 0
previous_checkpoint = -1
cmd_vel = 0.0
cmd_omega = 0.0
'''
Mahdi Ghanei and Ujjwal Gupta
'''
waypoint1 = rospy.get_param('/waypoint1')
waypoint2 = rospy.get_param('/waypoint2')
waypoint3 = rospy.get_param('/waypoint3')
waypoints = [waypoint1, waypoint2, waypoint3]

t_change = True
t_old = None
nav_status= None
previous_status = None
reject_first_status = "Yes"



def callback3(data):
	# global nav_status
	print("entered")

	global checkpoint, previous_checkpoint, nav_status, reject_first_status
	
	position = waypoints[checkpoint][0:3]
	orientation = waypoints[checkpoint][3:]
	# publish the waypoint to /move_base_simple/goal topic
	waypoint = PoseStamped()
	waypoint.pose.position.x = position[0]
	waypoint.pose.position.y = position[1]
	 
	waypoint.pose.orientation.x = orientation[0]
	waypoint.pose.orientation.y = orientation[1]
	waypoint.pose.orientation.z = orientation[2]
	waypoint.pose.orientation.w = orientation[3]

	waypoint.header.frame_id = "map"
	waypoint.header.stamp = rospy.get_rostime()

	# when new checkpoint comes, then only publish new waypoint 
	if reject_first_status != "Yes":
		stat = data.status_list
		print("length of status list", len(stat))
		nav_status = int(stat[-1].status)
		print("status_list", nav_status)

	
	
	if checkpoint != previous_checkpoint:
		print('publishing goal*********************************')
		# pub.publish(waypoint)
		sleep(2.0)
		print('publsihed goal after delay')
		pub.publish(waypoint)
		print("wait for status to update")
		sleep(5.0)
		reject_first_status = "No"
		
	previous_checkpoint = checkpoint
	if nav_status==3:
		print('\n\n\n****************************************checkpoint {', checkpoint, '} reached!')
		checkpoint = checkpoint + 1
		nav_status = None
		reject_first_status = "Yes"
		
		if checkpoint == 3:
			sleep(100.0)
		else:
			sleep(2.0)
	
	


def pubRobot(vel, omega):
	pose = Twist()
	pose.angular.z = omega
	pose.linear.x = vel
	pub_vel.publish(pose)
     	
def nav_waypoint():  #obstacle range
     	
	rospy.init_node('navigate_to_goal_point', anonymous=True)
	zero_vel =  int(sys.argv[1])

	if zero_vel>0:
		print('zeroing the velocity')
		oldtime = time()
		while (time() - oldtime) < 5:
			pubRobot(0,0)
		print('published zero')
	
	else:
		
		rospy.Subscriber('/move_base/status', GoalStatusArray, callback3, queue_size=1)
   	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
 
if __name__ == '__main__':
	nav_waypoint()

