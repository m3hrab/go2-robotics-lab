#!/bin/bash
set -e

source /opt/ros/humble/setup.bash
source /usr/share/gazebo/setup.sh

# ── Build the upstream Go2 workspace ─────────────────────────
cd /home/vscode/go2_ws
rosdep install --from-paths src --ignore-src -r -y || true
colcon build --symlink-install

# ── Install the sfl_robot Python package (editable) ─────────
# Codespaces always mounts the repo at /workspaces/<repo-name>.
REPO_ROOT="/workspaces/${GITHUB_REPOSITORY##*/}"
if [ ! -d "${REPO_ROOT}" ]; then
    REPO_ROOT="/workspaces/go2-robotics-lab"
fi
echo "Installing sfl_robot from ${REPO_ROOT}"
pip3 install -e "${REPO_ROOT}"
