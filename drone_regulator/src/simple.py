#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ardrone_autonomy.msg import Navdata
from geometry_msgs.msg import Twist
from velctrl import Step,Cont,Pulse

pub = None
battery = 20
hastag = False
engz = Cont()
engx = Cont()

def cb_navdata(data):
  global pub
  global battery
  global engz
  global hastag

  if int(data.batteryPercent/5) < battery:
    battery = int(data.batteryPercent/5)
    rospy.loginfo("Battery: {}-{}%".format(battery*5, (battery+1)*5))
  
  if data.tags_count > 0:
    hastag = True
    rospy.loginfo("Tag found {} {} {}".format(data.tags_xc[0], data.tags_yc[0], data.tags_orientation[0]))
    if engz.ready():
      e = 180-data.tags_orientation[0]
      if e > 5:
        engz.act(-2)
      elif e < -5:
        engz.act(2)
      else:
        engz.act(0)
  elif hastag and engz.ready():
    hastag = False
    engz.act(0)


  sendcmd = False
  vel = Twist()
  vel.linear.x = 0;
  vel.linear.y = 0;
  vel.linear.z = 0;
  vel.angular.x = 0;
  vel.angular.y = 0;
  vel.angular.z = 0;

  if engz.next():
    sendcmd = True
    vel.angular.z = engz.val()
  
  if sendcmd: 
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

  rospy.Subscriber("ardrone/navdata", Navdata, cb_navdata)

#  rospy.loginfo("GO!")
  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':
  listener()
