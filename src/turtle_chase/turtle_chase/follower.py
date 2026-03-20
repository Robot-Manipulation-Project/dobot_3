import math
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose


class Follower(Node):

    def __init__(self):
        super().__init__("follower")
        self.publisher = self.create_publisher(Twist, "/follower/cmd_vel", 10)
        self.leader_subscription = self.create_subscription(Pose, "/leader/pose", self.leader_callback, 10)
        self.follower_subscription = self.create_subscription(Pose, "/follower/pose", self.follower_callback, 10)
        self.leader_pose = None
        self.follower_pose = None        

    def leader_callback(self, msg):
        self.leader_pose = msg
        self.chase()

    def follower_callback(self, msg):
        self.follower_pose = msg

    def chase(self):
        if self.follower_pose is None or self.leader_pose is None:
            return
        
        dx = self.leader_pose.x - self.follower_pose.x
        dy = self.leader_pose.y - self.follower_pose.y
        
        cmd = Twist()
        cmd.linear.x = math.sqrt(dx**2 + dy**2)
        cmd.angular.z = math.atan2(dy, dx) - self.follower_pose.theta

        self.publisher.publish(cmd)
        self.get_logger().info(f"Chasing: {cmd}")
         

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = Follower()

            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
