#! /usr/bin/python

import rospy
import numpy as np
from nav_msgs.msg import Odometry
import tf

#===============================================================================
class AddNoise(object):
    '''
    Class that adds gaussian noise to the odometry and publishes it.
    '''
    
    #===========================================================================
    def __init__(self,lin_noise,ang_noise):
        '''
        Initializes publishers and subscribers.
        '''

        self.sub = rospy.Subscriber("/odom", Odometry, self.callback)
        self.pub_odom = rospy.Publisher("/new_odom", Odometry, queue_size = 1)
        
        self.odom_lin_sigma = lin_noise
        self.odom_ang_sigma = ang_noise
    
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
        """
        Publishes the odometry of the robot with gaussian noise.

        """
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
    
    if rospy.has_param("lin_noise"):
        lin_noise = rospy.get_param('lin_noise')
    else:
        lin_noise = 0.025
        
    if rospy.has_param("ang_noise"):    
        ang_noise = np.deg2rad(rospy.get_param('ang_noise'))
    else:
        ang_noise = np.deg2rad(2)
    
    # ROS init
    rospy.init_node('noisy_odometry', anonymous=True)
    node = AddNoise(lin_noise,ang_noise)
    rospy.spin()
