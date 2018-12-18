#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Example():

  def __init__(self):
    self.has_to_stop_robot = False
    # Initialize ROS node
    rospy.init_node('example', anonymous=True)
    # Ros publisher
    self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    # ROS subscriber
    rospy.Subscriber("wall_sensor/scan", LaserScan, self.wall_sensor_cb)
    # Declare shutdown hook
    rospy.on_shutdown(self.shutdown)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
      if self.has_to_stop_robot:
        self.stop_robot()
      else:
        # Create velocity message
        vel_msg = Twist()
        vel_msg.linear.x = 0.1
        vel_msg.angular.z = 0.05
        # Publish message
        self.pub.publish(vel_msg)
      rate.sleep()
  
  def wall_sensor_cb(self, msg):
    # Stop robot if measurement was detected
    self.has_to_stop_robot = True if msg.ranges[0] < 1.0 else False
  
  def stop_robot(self):
    rospy.loginfo("Stopping robot")
    self.pub.publish(Twist())

  def shutdown(self):
    self.stop_robot()


if __name__ == '__main__':
  try:
    Example()
  except rospy.ROSInterruptException:
    pass