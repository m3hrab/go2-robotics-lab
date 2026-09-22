#!/bin/bash
set -e

source /opt/ros/humble/setup.bash
source /usr/share/gazebo/setup.sh

cd /home/vscode/go2_ws
rosdep install --from-paths src --ignore-src -r -y || true
colcon build --symlink-install

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
pip3 install -e "${REPO_ROOT}"
