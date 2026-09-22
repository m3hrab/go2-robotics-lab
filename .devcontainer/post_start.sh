#!/bin/bash
set -euo pipefail

sleep 8

# ── Environment ──────────────────────────────────────────────
source /opt/ros/humble/setup.bash
source /usr/share/gazebo/setup.sh
source /home/vscode/go2_ws/install/setup.bash
export ROS_DOMAIN_ID=30
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export LIBGL_ALWAYS_SOFTWARE=1

# ── Virtual Display ──────────────────────────────────────────
if ! pgrep -f "Xvfb :99" > /dev/null; then
    Xvfb :99 -screen 0 1280x720x24 &
    sleep 2
fi
export DISPLAY=:99

# ── Python package ───────────────────────────────────────────
REPO_ROOT="/workspaces/${GITHUB_REPOSITORY##*/}"
if [ ! -d "${REPO_ROOT}" ]; then
    REPO_ROOT="/workspaces/go2-robotics-lab"
fi

if [ -d "${REPO_ROOT}" ]; then
    echo "Installing sfl_robot from ${REPO_ROOT}"
    pip3 install -e "${REPO_ROOT}" || true
fi

# ── Gazebo ───────────────────────────────────────────────────
if pgrep -f "go2_config.*gazebo" > /dev/null; then
    echo "Gazebo already running"
else
    cd /home/vscode/go2_ws
    nohup ros2 launch go2_config gazebo.launch.py rviz:=false \
        > /tmp/gazebo.log 2>&1 &
    echo "Gazebo launched (log: /tmp/gazebo.log)"
fi

# ── rosbridge ────────────────────────────────────────────────
if pgrep -f rosbridge_websocket > /dev/null; then
    echo "rosbridge already running"
else
    nohup ros2 launch rosbridge_server rosbridge_websocket_launch.xml \
        > /tmp/rosbridge.log 2>&1 &
    echo "rosbridge launched (log: /tmp/rosbridge.log)"
fi
