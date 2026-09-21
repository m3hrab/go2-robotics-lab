from sfl_robot.robot import Robot

robot = Robot(config="sfl_robot/config.yaml")
robot.walk_to(1, 0)
robot.turn(90)
robot.walk_to(1, 1)
