#!/bin/bash
set -e
source /opt/ros/humble/setup.bash
cd /home/vscode/go2_ws
rosdep install --from-paths src --ignore-src -r -y || true
colcon build --symlink-install
