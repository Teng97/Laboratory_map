#! /usr/bin/python

import rospy
import numpy as np
from nav_msgs.msg import Odometry
import tf

#===============================================================================
class AddNoise(object):

    #===========================================================================
    def __init__(self):

        self.sub = rospy.Subscriber("/odom", Odometry, self.callback)
        self.pub_odom = rospy.Publisher("/new_odom", Odometry, queue_size = 1)
        
        self.odom_lin_sigma = rospy.get_param('odom_lin_sigma')
        self.odom_ang_sigma = np.deg2rad(rospy.get_param('odom_ang_sigma'))

    
    #===========================================================================    
    def angle_wrap(self,ang):
        """
        Return the angle normalized between [-pi, pi].

        Works with numbers and numpy arrays.

        """
        ang = ang % (2 * np.pi)
        if (isinstance(ang, int) or isinstance(ang, float)) and (ang > np.pi):
            ang -= 2 * np.pi
        elif isinstance(ang, np.ndarray):
            ang[ang > np.pi] -= 2 * np.pi
        return ang
    
    #===========================================================================
    def callback(self,msg):
        
        # Add Gaussian noise to odometry
        
        noise_x = np.random.randn(1)
        noise_y = np.random.randn(1)
        noise_angle = np.random.randn(1)
            
        odom = msg
        odom.twist.twist.linear.x += noise_x * self.odom_lin_sigma
        odom.twist.twist.linear.y += noise_y * self.odom_lin_sigma
        odom.twist.twist.angular.z = self.angle_wrap(odom.twist.twist.angular.z + noise_angle * self.odom_ang_sigma)
            
        self.pub_odom.publish(odom)
            
                     
if __name__ == '__main__':
    # ROS init
    rospy.init_node('noisy_odometry', anonymous=True)
    node = AddNoise()
    rospy.spin()
