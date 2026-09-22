#!/bin/bash
sleep 5
source /opt/ros/humble/setup.bash
source /usr/share/gazebo/setup.sh
source /home/vscode/go2_ws/install/setup.bash
export ROS_DOMAIN_ID=30
export LIBGL_ALWAYS_SOFTWARE=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if command -v pip3 > /dev/null 2>&1; then
    echo "Installing editable Python package from ${REPO_ROOT}"
    pip3 install -e "${REPO_ROOT}"
else
    echo "pip3 is not installed. Rebuild the dev container to install python3-pip." >&2
    exit 1
fi

if pgrep -f "go2_config.*gazebo" > /dev/null; then
    echo "Gazebo already running"
else
    cd /home/vscode/go2_ws
    nohup ros2 launch go2_config gazebo.launch.py rviz:=false > /tmp/gazebo.log 2>&1 &
fi

if pgrep -f rosbridge_websocket > /dev/null; then
    echo "rosbridge already running"
else
    nohup ros2 launch rosbridge_server rosbridge_websocket_launch.xml > /tmp/rosbridge.log 2>&1 &
fi
