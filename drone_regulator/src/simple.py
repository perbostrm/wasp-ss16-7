#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ardrone_autonomy.msg import Navdata
from geometry_msgs.msg import Twist
from velctrl import Step,Cont,Pulse

pub = None
battery = 20
hastag = False
engz = Pulse(5, 30, 0)
engx = Pulse(5, 30, 10)
engy = Pulse(5, 30, 20)

def cb_navdata(data):
  global pub
  global battery
  global engz
  global engx
  global engy
  global hastag
    
  d_x = 0
  d_y = 0

  if int(data.batteryPercent/5) != battery:
    battery = int(data.batteryPercent/5)
    rospy.loginfo(data.batteryPercent)
    rospy.loginfo("Battery: {}-{}%".format(battery*5, (battery+1)*5))
  
  if data.tags_count > 0:
    hastag = True
    #rospy.loginfo("Tag found {} {} {}".format(data.tags_xc[0], data.tags_yc[0], data.tags_orientation[0]))
    if engz.ready():
      e = data.tags_orientation[0]-180
      if e > 5:
        engz.act(1)
      elif e < -5:
        engz.act(-1)
      else:
        engz.act(0)

    ref_x = 500
    ref_y = 500
    e_x = data.tags_xc[0]-ref_x
    e_y = data.tags_yc[0]-ref_y
    d_x = -0.01*e_x
    d_y = -0.01*e_y

    if engx.ready():
        if d_x == 0:
            engx.act(0)
        else:
            engx.act(1)

    if engy.ready():
        if d_y == 0:
            engy.act(0)
        else:
            engy.act(1)

  elif hastag and engz.ready():
    hastag = False
    engx.act(0)
    engy.act(0)
    engz.act(0)


  sendcmd = False
  vel = Twist()
  vel.linear.x = 0;
  vel.linear.y = 0;
  vel.linear.z = 0;
  vel.angular.x = 1;
  vel.angular.y = 1;
  vel.angular.z = 0;

  if engz.next():
    sendcmd = True
    vel.angular.z = engz.val()

  if engx.next():
    sendcmd = True
    vel.linear.x = -d_y*engx.val()

  if engy.next():
    sendcmd = True
    vel.linear.y = d_x*engy.val()

  
  if sendcmd: 
   # rospy.loginfo("Z: {} X: {} Y: {}".format(engz.val(), engx.val(), engy.val()));
    if vel.linear.x < -1:
        vel.linear.x = -1
    if vel.linear.x > 1:
        vel.linear.x = 1
    if vel.linear.y < -1:
        vel.linear.y = -1
    if vel.linear.y > 1:
        vel.linear.y = 1
    rospy.loginfo("{} {} {}".format(vel.linear.x, vel.linear.y, vel.angular.z))
  pub.publish(vel)
#  else:
#    rospy.loginfo("No publish")

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
