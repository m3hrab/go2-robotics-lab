FROM mcr.microsoft.com/devcontainers/base:jammy

USER root
ENV LIBGL_ALWAYS_SOFTWARE=1

RUN apt-get update && apt-get install -y \
    software-properties-common curl gnupg2 lsb-release git wget gpg \
 && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository universe && apt-get update

RUN mkdir -p /etc/apt/keyrings \
 && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /etc/apt/keyrings/ros-archive-keyring.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu jammy main" \
    > /etc/apt/sources.list.d/ros2.list

RUN curl -sSL https://packages.osrfoundation.org/gazebo.gpg \
    --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable jammy main" \
    > /etc/apt/sources.list.d/gazebo-stable.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-desktop ros-humble-gazebo-* gz-fortress \
    python3-colcon-common-extensions ros-humble-rmw-cyclonedds-cpp \
    ros-humble-gazebo-ros2-control ros-humble-xacro \
    ros-humble-robot-localization ros-humble-ros2-controllers ros-humble-ros2-control \
    ros-humble-rosbridge-suite ffmpeg \
    python3-rosdep python3-vcstool \
 && rm -rf /var/lib/apt/lists/*

RUN rosdep init || true

RUN echo "source /opt/ros/humble/setup.bash" >> /etc/skel/.bashrc \
 && echo "source /usr/share/gazebo/setup.sh" >> /etc/skel/.bashrc \
 && echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> /etc/skel/.bashrc \
 && echo 'export ROS_DOMAIN_ID=30' >> /etc/skel/.bashrc

RUN mkdir -p /home/vscode/go2_ws/src && chown -R vscode:vscode /home/vscode/go2_ws
USER vscode
WORKDIR /home/vscode/go2_ws/src
RUN git clone https://github.com/anujjain-dev/unitree-go2-ros2.git

USER root
RUN rosdep update
RUN bash -c "source /opt/ros/humble/setup.bash && cd /home/vscode/go2_ws && rosdep install --from-paths src --ignore-src -r -y" || true

USER vscode
WORKDIR /home/vscode/go2_ws
RUN bash -c "source /opt/ros/humble/setup.bash && colcon build --symlink-install"

RUN echo 'source ~/go2_ws/install/setup.bash' >> ~/.bashrc
