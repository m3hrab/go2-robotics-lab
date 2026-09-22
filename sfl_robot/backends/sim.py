import math
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class SimBackend(Node):
    def __init__(self):
        if not rclpy.ok():
            rclpy.init(args=None)
        super().__init__('sfl_robot_sim')

        self._cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self._spin_for(0.5)

    def _spin_for(self, seconds: float):
        end = time.time() + seconds
        while time.time() < end:
            rclpy.spin_once(self, timeout_sec=0.05)

    def _publish_for(self, twist: Twist, seconds: float):
        end = time.time() + seconds
        while time.time() < end:
            self._cmd_pub.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.05)
        self._cmd_pub.publish(Twist())

    def walk_to(self, x, y, speed=0.2):
        distance = (x ** 2 + y ** 2) ** 0.5
        if distance == 0:
            return
        t = Twist()
        t.linear.x = speed
        self._publish_for(t, distance / speed)

    def turn(self, deg, angular_speed=0.3):
        if deg == 0:
            return
        t = Twist()
        t.angular.z = angular_speed if deg > 0 else -angular_speed
        self._publish_for(t, abs(math.radians(deg)) / angular_speed)

    def stand(self):
        pass

    def sit(self):
        pass

    def get_camera_image(self):
        raise RuntimeError("Sensors not enabled in this build. Skipped for now.")

    def get_obstacle_distance(self):
        return float('inf')
