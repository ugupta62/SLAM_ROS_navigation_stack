# SLAM_ROS_navigation_stack
This project navigates the Turtlebot3 to a given waypoints in waypoints.yaml using ROS nav_stack for avoiding static and dynamic obstacle in the provided environment -map.pgm.



Commands to run on the robot (the master):
- run the camera bringup: ```roslaunch turtlebot3_bringup turtlebot3_camera_robot.launch```

Commands to run on the PC (the slave):
- run the navigation stack: ```roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=/home/burger/catkin_ws/src/gryffindor_final_demo/map.yaml```
- run the projects launch file in the project directory: ```roslaunch navigate_to_waypoints.launch my_args:=0```
