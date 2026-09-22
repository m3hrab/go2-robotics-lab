import os

import yaml


class RobotError(Exception):
    """Readable error surfaced to students. Never a raw ROS/Gazebo traceback."""


class Robot:
    def __init__(self, config=None):
        if config is None:
            config = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config) as f:
            cfg = yaml.safe_load(f)

        target = cfg.get("target")
        if target == "sim":
            from sfl_robot.backends.sim import SimBackend
            self._backend = SimBackend()
        elif target == "real":
            from sfl_robot.backends.real import RealBackend
            self._backend = RealBackend()
        else:
            raise RobotError(f"Unknown target '{target}' in config.yaml")

    def walk_to(self, x, y):
        """Walk to coordinate (x, y) in meters.
        Example: robot.walk_to(2, 0)
        """
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise RobotError("walk_to expects two numbers, e.g. robot.walk_to(2, 0)")
        self._backend.walk_to(x, y)

    def turn(self, deg):
        """Turn in place by deg degrees. Positive is left, negative is right."""
        if not isinstance(deg, (int, float)):
            raise RobotError("turn expects a number of degrees, e.g. robot.turn(90)")
        self._backend.turn(deg)

    def stand(self):
        self._backend.stand()

    def sit(self):
        self._backend.sit()

    def get_camera_image(self):
        return self._backend.get_camera_image()

    def get_obstacle_distance(self):
        return self._backend.get_obstacle_distance()
