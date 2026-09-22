"""Smoke tests for sfl_robot. Run with: pytest tests/ -v"""

import pytest

from sfl_robot.robot import Robot, RobotError


def test_unknown_target_raises(tmp_path):
    cfg = tmp_path / "bad.yaml"
    cfg.write_text("target: nonsense\n")
    with pytest.raises(RobotError):
        Robot(config=str(cfg))


def test_walk_to_rejects_strings():
    # We don't build a real Robot here (needs ROS); test the guard directly
    from sfl_robot.robot import Robot
    r = object.__new__(Robot)
    with pytest.raises(RobotError):
        Robot.walk_to(r, "a", 1)


def test_turn_rejects_strings():
    from sfl_robot.robot import Robot
    r = object.__new__(Robot)
    with pytest.raises(RobotError):
        Robot.turn(r, "left")