from unittest.mock import MagicMock, patch
from sfl_robot.robot import Robot, RobotError
import pytest


def test_walk_to_rejects_non_numeric():
    with patch("sfl_robot.backends.sim.SimBackend"):
        robot = Robot()
        with pytest.raises(RobotError):
            robot.walk_to("a", 0)