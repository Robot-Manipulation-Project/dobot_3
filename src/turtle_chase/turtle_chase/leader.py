import random

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool


class Leader(Node):

    def __init__(self):
        super().__init__("leader")
        self.publisher = self.create_publisher(Twist, "/leader/cmd_vel", 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.forward_velocity = 1.0
        self.service = self.create_service(SetBool, "/turbo", self.service_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = self.forward_velocity
        msg.angular.z = random.uniform(-3.14, 3.14)
        self.publisher.publish(msg)
        self.get_logger().info(f"Publishing: {msg}")


    def service_callback(self, request, response):
        if request.data:
            self.forward_velocity = 2.0
        else:
            self.forward_velocity = 1.0

        response.success = True  # Set to True or False based on your logic

        if request.data:
            response.message = "Turbo mode enabled"
        else:
            response.message = "Turbo mode disabled"
        return response

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = Leader()
            rclpy.spin(node)

    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()
