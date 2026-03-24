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
        self.timer = self.create_timer(0.1, self.chase)  # Control loop at 10Hz

    def leader_callback(self, msg):
        self.leader_pose = msg

    def follower_callback(self, msg):
        self.follower_pose = msg

    def chase(self):
        if self.follower_pose is None or self.leader_pose is None:
            return

        dx = self.leader_pose.x - self.follower_pose.x
        dy = self.leader_pose.y - self.follower_pose.y
        distance = math.sqrt(dx**2 + dy**2)

        desired_angle = math.atan2(dy, dx)

        angle_error = desired_angle - self.follower_pose.theta
        angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi
        
        cmd = Twist()
 
        cmd.linear.x = min(2.0, max(0.1, distance * 1.5))
        
        cmd.angular.z = min(3.0, max(-3.0, angle_error * 3.0))
        
        if distance < 0.2:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
        
        self.publisher.publish(cmd)
        self.get_logger().info(f'Dist: {distance:.2f}, Angle Err: {angle_error:.2f}, '
                              f'Vel: {cmd.linear.x:.2f}, Ang: {cmd.angular.z:.2f}')

def main(args=None):
    try:
        rclpy.init(args=args)
        node = Follower()
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()