# Gazebo-Simulation

In this repository, you will find robot simulations created using Gazebo.

## Overview

In this repository, I am uploading the URDF models of the robots along with their Gazebo simulations.

The environments are structured as catkin workspaces within a ROS Noetic environment on Ubuntu 20.04. The software might not work or compile outside of this setup.

While you can use the ROS Catkin make build system, it is preferable to use catkin tools. The build commands provided below assume you are using catkin tools.

The two workspaces must be in separate directories on your system.

## Installation

You can install ROS Noetic by following the instructions at:

[https://wiki.ros.org/noetic/Installation/Ubuntu](https://wiki.ros.org/noetic/Installation/Ubuntu)

During the installation of ROS, it is recommended to install the following packages:

`sudo apt-get install ros-noetic-joy sudo apt-get install ros-noetic-rplidar-ros sudo apt-get install ros-noetic-hector-slam sudo apt-get install ros-noetic-teleop-twist-keyboard`

For catkin tools, use these commands:

`sudo apt-get install python3-catkin-tools sudo apt-get install python3-catkin-pkg python3-catkin-pkg-modules`

## Launching the Car Simulation

After downloading the repository and extracting the content to your Home directory (not mandatory, but preferred), open the `sorcio_2_ws` directory in the terminal and run the following commands:

`catkin build  source devel/setup.bash  roslaunch test_description gazebo.launch`

If you want to control the car via the keyboard, open another terminal and run:

`rosrun teleop_twist_keyboard teleop_twist_keyboard.py`

If you want a "better" view of what is happening around the robot (in terms of sensor data), open yet another terminal and run:

`cd sorcio_2_ws  source devel/setup.bash  roslaunch test_description display.launch`

## Launching the Spotty Simulation

After downloading the repository and extracting the content to your Home directory (again, not mandatory but preferred), open the `spotty_sim_ws` directory in the terminal and execute the following commands:


`cd spotty_sim_ws  catkin build  source devel/setup.bash  roslaunch spotty run_spotty_gazebo.launch`

Executing these commands will start both Gazebo and RViz.

If the robot has flipped over in Gazebo, press **CTRL+R** to reset the world. This will reposition the robot correctly.

**PS:**  
If you encounter issues with the `catkin build` command, run the following in the terminal:


`rm -rf .catkin_tools`

If you have any questions, feel free to contact me and we'll work through them together.

Here are some links to repositories that might be useful:

- This repository is the basis for the Spotty simulation. Some modifications have been made, but essentially you can review the code here if you want to add something:  
    [lnotspotl/notspot_sim_py](https://github.com/lnotspotl/notspot_sim_py/tree/main)
- This is a very interesting repository that uses Pybullet for simulation and RL algorithms to enable the robot to walk on various types of terrain. Take a look—maybe you can understand it better than I do:  
    [OpenQuadruped/spot_mini_mini](https://github.com/OpenQuadruped/spot_mini_mini/tree/spot)

If you have trouble working with Gazebo, we can try switching to Pybullet.
