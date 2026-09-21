import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SimBackend(Node):
    def __init__(self):
        if not rclpy.ok():
            rclpy.init(args=None)
        super().__init__('sfl_robot_sim')
        self._cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def _publish_for(self, twist, seconds):
        end = time.time() + seconds
        while time.time() < end:
            self._cmd_pub.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.05)
        self._cmd_pub.publish(Twist())

    def walk_to(self, x, y, speed=0.2):
        distance = (x**2 + y**2) ** 0.5
        t = Twist()
        t.linear.x = speed
        self._publish_for(t, distance / speed)

    def turn(self, deg, angular_speed=0.3):
        import math
        t = Twist()
        t.angular.z = angular_speed if deg > 0 else -angular_speed
        self._publish_for(t, abs(math.radians(deg)) / angular_speed)

    def stand(self):
        pass  # check /body_pose topic — likely how CHAMP handles stand/sit

    def sit(self):
        pass

    def get_camera_image(self):
        raise NotImplementedError("no camera topic in current topic list — confirm go2 has one, or drop from lesson 2")

    def get_obstacle_distance(self):
        raise NotImplementedError("check /foot_contacts for contact-based avoidance, or add a lidar/range sensor to the URDF/world")
