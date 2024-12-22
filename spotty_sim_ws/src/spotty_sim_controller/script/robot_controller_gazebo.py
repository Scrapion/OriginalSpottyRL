#!/usr/bin/env python3

import rospy

from sensor_msgs.msg import Imu
from std_msgs.msg import Float64

from RobotController import Robot_Controller
from InverseKineamtics import robot_ik

USE_IMU = False
RATE = 60

rospy.init_node("robot_controller", anonymous=True)

# Robot geometry
body = [0.3047, 0.078]  # cambiare le misure
legs = [0.01, 0.024, 0.10675, 0.130]  # cambiare le misure

spotty_robot = Robot_Controller.Robot(body=body, legs=legs, imu=USE_IMU)
ik = robot_ik.InverseKinematics(body_dimension=body, leg_dimension=legs)

command_topics = ["/spotty_controller/front_right_shoulder_joint/command",
                  "/spotty_controller/front_right_leg_joint/command",
                  "/spotty_controller/front_right_foot_joint/command",

                  "/spotty_controller/front_left_shoulder_joint/command",
                  "/spotty_controller/front_left_leg_joint/command",
                  "/spotty_controller/front_left_foot_joint/command",

                  "/spotty_controller/rear_right_shoulder_joint/command",
                  "/spotty_controller/rear_right_leg_joint/command",
                  "/spotty_controller/rear_right_foot_joint/command",

                  "/spotty_controller/rear_left_shoulder_joint/command",
                  "/spotty_controller/rear_left_leg_joint/command",
                  "/spotty_controller/rear_left_foot_joint/command"]

publishers = []

for i in range(len(command_topics)):
    publishers.append(rospy.Publisher(command_topics[i], Float64, queue_size=1))

if USE_IMU:
    rospy.Subscriber("spotty_imu/base_link_orientation", Imu, spotty_robot.imu_orientation)

rate = rospy.Rate(RATE)

"""
del body
del legs
del command_topics
del USE_IMU
del RATE
"""

while not rospy.is_shutdown():
    leg_positions = spotty_robot.run()
    spotty_robot.change_controller()

    dx = spotty_robot.state.body_local_position[0]
    dy = spotty_robot.state.body_local_position[1]
    dz = spotty_robot.state.body_local_position[2]

    roll = spotty_robot.state.body_local_orientation[0]
    pitch = spotty_robot.state.body_local_orientation[1]
    yaw = spotty_robot.state.body_local_orientation[2]

    try:
        joint_angles = ik.inverse_kinematics(leg_positions, dx, dy, dz, roll, pitch, yaw)

        for i in range(len(joint_angles)):
            publishers[i].publish(joint_angles[i])

    except:
        print("Non riesco a inviare i valori degli angoli")

    rate.sleep()
