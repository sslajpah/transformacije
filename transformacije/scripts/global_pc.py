#!/usr/bin/env python  
import rospy
import tf2_ros
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2

from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud



class global_pointcloud():

    def __init__(self):
        
        # rospy.Subscriber('topic_name', varType, callback)
        self.sub = rospy.Subscriber('/cloud', PointCloud2, self.pc_local2global)
        self.pub = rospy.Publisher('/cloud_global',PointCloud2, queue_size=10)

        # tf listener
        self.tfBuffer = tf2_ros.Buffer() # buffer 10 sekund
        self.listener = tf2_ros.TransformListener(self.tfBuffer)
        
        self.ctrl_c = False
        rospy.on_shutdown(self.shutdownhook)

    def pc_local2global(self,cloud_in):
        
        # get transform between laser and world
        transform = self.tfBuffer.lookup_transform("world","laser",rospy.Time(0))

        # transform point cloud
        # sudo apt install ros-<ros distro>-tf2-sensor-msgs
        cloud_out = do_transform_cloud(cloud_in, transform)
        #print(transform)

        #for p in point_cloud2.read_points(cloud_out, field_names = ("x", "y", "z"), skip_nans=True):
        for p in point_cloud2.read_points(cloud_out, field_names = ("z"), skip_nans=True):
            print(p)

        self.pub.publish(cloud_out)

    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        # this code is run at ctrl + c

        self.ctrl_c = True

if __name__ == '__main__':
    # initialise node
    rospy.init_node('get_laser_world')
    # initialise class
    pc_world = global_pointcloud()
 
    try:
        # loop
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
