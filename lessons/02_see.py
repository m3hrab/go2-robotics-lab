"""Lesson 02 — See with the robot's camera.

Reads one frame from the front camera and reports basic info.

Run:  python3 lessons/02_see.py
"""

from sfl_robot.robot import Robot, RobotError


def main():
    robot = Robot(config="sfl_robot/config.yaml")

    try:
        image = robot.get_camera_image()
    except (RobotError, RuntimeError) as exc:
        print(f"Camera not available: {exc}")
        print("Tip: the upstream go2_config URDF disables the camera plugin.")
        print("     Enable camera.xacro in go2_description or skip this lesson.")
        return

    print("Got a camera frame!")
    print(f"  Resolution : {image.width} x {image.height}")
    print(f"  Encoding   : {image.encoding}")


if __name__ == "__main__":
    main()