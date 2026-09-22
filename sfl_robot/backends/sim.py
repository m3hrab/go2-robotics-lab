import math
import struct
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan, PointCloud2


class SimBackend(Node):
    def __init__(self):
        if not rclpy.ok():
            rclpy.init(args=None)
        super().__init__('sfl_robot_sim')

        self._cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self._latest_scan: LaserScan | None = None
        self._latest_cloud: PointCloud2 | None = None
        self._latest_image: Image | None = None

        self.create_subscription(LaserScan, '/scan', self._scan_cb, 10)
        self.create_subscription(PointCloud2, '/velodyne_points', self._cloud_cb, 10)
        self.create_subscription(Image, '/camera/image_raw', self._image_cb, 10)

        self._spin_for(0.5)

    # ── Callbacks ───────────────────────────────────────────
    def _scan_cb(self, msg: LaserScan):
        self._latest_scan = msg

    def _cloud_cb(self, msg: PointCloud2):
        self._latest_cloud = msg

    def _image_cb(self, msg: Image):
        self._latest_image = msg

    # ── Helpers ─────────────────────────────────────────────
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

    # ── Motion ──────────────────────────────────────────────
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

    # ── Sensors ─────────────────────────────────────────────
    def get_camera_image(self):
        self._spin_for(0.5)
        if self._latest_image is None:
            raise RuntimeError(
                "No image on /camera/image_raw. The upstream go2_config "
                "URDF does not enable the camera plugin by default. "
                "Either enable the camera xacro or skip Lesson 02."
            )
        return self._latest_image

    def get_obstacle_distance(self):
        self._spin_for(0.5)

        if self._latest_scan is not None:
            valid = [r for r in self._latest_scan.ranges if math.isfinite(r)]
            if valid:
                return min(valid)

        if self._latest_cloud is not None:
            return self._min_range_from_cloud(self._latest_cloud)

        return float('inf')

    @staticmethod
    def _min_range_from_cloud(cloud: PointCloud2, half_angle_deg: float = 30.0) -> float:
        if cloud.width * cloud.height == 0:
            return float('inf')

        offsets = {f.name: f.offset for f in cloud.fields}
        if 'x' not in offsets or 'y' not in offsets:
            return float('inf')

        x_off, y_off = offsets['x'], offsets['y']
        point_step = cloud.point_step
        data = cloud.data

        cos_limit = math.cos(math.radians(half_angle_deg))
        min_r = float('inf')

        for i in range(0, len(data), point_step):
            try:
                x = struct.unpack_from('<f', data, i + x_off)[0]
                y = struct.unpack_from('<f', data, i + y_off)[0]
            except struct.error:
                continue
            if not (math.isfinite(x) and math.isfinite(y)):
                continue
            r = math.hypot(x, y)
            if r == 0:
                continue
            if x / r >= cos_limit and r < min_r:
                min_r = r

        return min_r
