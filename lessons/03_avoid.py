"""Lesson 03 — Avoid obstacles using the LiDAR.

Walks forward until an obstacle is within SAFE_DISTANCE, then turns.

Run:  python3 lessons/03_avoid.py
"""

import time

from sfl_robot.robot import Robot, RobotError

SAFE_DISTANCE = 0.6
TURN_DEGREES = 90


def main():
    robot = Robot(config="sfl_robot/config.yaml")

    print("Starting obstacle avoidance. Press Ctrl+C to stop.")
    try:
        while True:
            distance = robot.get_obstacle_distance()
            print(f"Closest obstacle: {distance:.2f} m")

            if distance < SAFE_DISTANCE:
                print("Obstacle ahead — turning!")
                robot.turn(TURN_DEGREES)
            else:
                robot.walk_to(0.5, 0)

            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except RobotError as exc:
        print(f"Robot error: {exc}")


if __name__ == "__main__":
    main()