#include "ros/ros.h"
#include <fstream>
#include <iostream>

void subscr (const wasp_custom_msgs::object_loc& location){
  char data[100];

  ofstream outfile;
  outfile.open("WASP_Group7_Result.dat");

  cout << "Writing to the file" << endl;
  outfile << location.ID << endl;
  outfile << location.point.x << endl;
  outfile << location.point y << endl;
  outfile << location.point z << endl;
  outfile << endl;
  outfile.close();

  //    wasp_custom_msgs::object_loc location;
  //location.ID = detection.id;
  // location.point.x = translation(0);
  // location.point.y = translation(1);
  // location.point.z = translation(2);
  // object_location_pub.publish(location);

}


int main (int argc, char** argv){
 // Load all parameters from PCL_ground_removal.yaml
 //system("rosparam load ~/catkin_ws/src/task3_pcl/parameters/PCL_ground_removal.yaml /PCL_ground_removal");
 // Initialize ROS with NoSigintHandler
  ros::init (argc, argv, "listener");//PCL_ground_removal", ros::init_options::NoSigintHandler);
  ros::NodeHandle nh;
 // In case of ctrl-c handle that with mySigintHandler
 //signal(SIGINT, mySigintHandler);

 // Create a ROS subscriber for the input point cloud
 ros::Subscriber sub = nh.subscribe ("chatter", 100, subscr);
 // Spin
 ros::spin ();
}
