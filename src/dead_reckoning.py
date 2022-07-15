#!/usr/bin/python3
import tf
import rospy
from visualization_msgs.msg import Marker
from sensor_msgs.msg import Image, Imu
from geometry_msgs.msg import Pose
import message_filters

class XYZ:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def update(self, dv, dt):
        self.x += dv.x * dt
        self.y += dv.y * dt
        self.z += dv.z * dt

class DeadReckoning:
    def __init__(self):
        rospy.init_node("dead_reckon")
        self.current_velocity = XYZ()
        self.current_position = XYZ()
        self.current_euler = XYZ()
        self.nsecs = rospy.Time.now().nsecs
        self.count = 0
        self.pub_pose = rospy.Publisher('/processed_pose', Pose, queue_size=8)

    def callback(self, accel, gyro):
        self.count += 1
        nsecs = rospy.Time.now().nsecs
        dt = abs(nsecs - self.nsecs) / 1e9
        self.nsecs = nsecs
        # "integrate" velocity, position, and orientation
        self.current_velocity.update(accel.linear_acceleration, dt)
        self.current_position.update(self.current_velocity, dt)
        self.current_euler.update(gyro.angular_velocity, dt)
        orientation = tf.transformations.quaternion_from_euler(self.current_euler.x, self.current_euler.y, self.current_euler.z)
        # Create reference frame with position and orientation
        pose = Pose()
        pose.position.x = self.current_position.x
        pose.position.y = self.current_position.y
        pose.position.z = self.current_position.z
        pose.orientation.x = orientation[0] 
        pose.orientation.y = orientation[1] 
        pose.orientation.z = orientation[2] 
        pose.orientation.w = orientation[3]
        # publish pose to rostopics
        self.pub_pose.publish(pose)

    def track(self):
        gyro_sub = message_filters.Subscriber("/device_0/sensor_2/Gyro_0/imu/data", Imu)
        accel_sub = message_filters.Subscriber("/device_0/sensor_2/Accel_0/imu/data", Imu)
        sync = message_filters.ApproximateTimeSynchronizer([accel_sub, gyro_sub], 1, 2)
        sync.registerCallback(self.callback)
        rospy.spin()


if __name__ == "__main__":
    tracker = DeadReckoning()
    tracker.track()
