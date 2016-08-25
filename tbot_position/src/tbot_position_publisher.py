#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Pose2D
import time

def position_callback(data):
    # Extract the 2D Position (x, y, theta of the tbot)
    pose2D = Pose2D()
    pose2D.x = data.pose.pose.position.x
    pose2D.y = data.pose.pose.position.y

    # Orientation
    or_x = data.pose.pose.orientation.x
    or_y = data.pose.pose.orientation.y
    or_z = data.pose.pose.orientation.z
    or_w = data.pose.pose.orientation.w

    # TODO: Implement correct transform for theta
    pose2D.theta = 1;#atan2(2*or_w*or_z, or_w*or_w - or_z*or_z)

    pub1.publish(pose2D)

# Intializes everything
def start():
    # Create Global Publishers
    global pub1
    #Initialize current node with some name
    rospy.init_node('tbot_position_publisher')
    #Assigin publisher that publishes the position in 2D (x, y, theta)
    pub1 = rospy.Publisher('/tbot_pose2D', Pose2D, queue_size=1)
    #subscribe to list of goals from rviz interaction package
    rospy.Subscriber("/robot_pose_ekf/odom_combined", PoseWithCovarianceStamped, position_callback)
    #This keeps the function active till node are shurdown.
    rospy.spin()

#Main function
if __name__ == '__main__':
	start()
