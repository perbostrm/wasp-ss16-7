#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ardrone_autonomy.msg import Navdata
from geometry_msgs.msg import Twist

pub = None

def callback(data):
  global pub
  if data.tags_count > 0:
    rospy.loginfo("Tag found {} {} {}".format(data.tags_xc[0], data.tags_yc[0], data.tags_orientation[0]))
    e = data.tags_orientation[0]
    d = -e
    vel = Twist()
    vel.linear.x = 0;
    vel.linear.y = 0;
    vel.linear.z = 0;
    vel.angular.x = 0;
    vel.angular.y = 0;
    vel.angular.z = d/360;
    rospy.loginfo(vel)
    pub.publish(vel)
    
def listener():
  global pub
  pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

  # In ROS, nodes are uniquely named. If two nodes with the same
  # node are launched, the previous one is kicked off. The
  # anonymous=True flag means that rospy will choose a unique
  # name for our 'listener' node so that multiple listeners can
  # run simultaneously.
  rospy.init_node('ardrone_ctrl', anonymous=True)

  rospy.Subscriber("ardrone/navdata", Navdata, callback)

  rospy.loginfo("GO!")
  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':
  listener()
