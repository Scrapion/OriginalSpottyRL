#!/usr/bin/env python3

import rospy
import numpy as np
from RobotController.PID_Controller import PID_controller
from RoboticsUtilities.transformation import rotxyz


class Rest_controller(object):

    def __init__(self, neutral_stance):
        self.neutral_stance = neutral_stance

        self.pid_controller = PID_controller(kp=0.75, ki=2.29, kd=0.0)
        self.use_imu = False
        self.pid_controller.reset()

    @property
    def default_stance(self):
        return self.neutral_stance

    def step(self, state, command):
        temp = self.default_stance
        temp[2] = [command.robot_height] * 4

        if self.use_imu:
            rospy.loginfo(f"Rest Controller - Use roll/pitch compensation: {self.use_imu}")

            compensation = self.pid_controller.run(state.imu_roll, state.imu_pitch)
            roll_compensation = -compensation[0]
            pitch_compensation = -compensation[1]

            rot = rotxyz(roll_compensation, pitch_compensation, 0)

            temp = np.matmul(rot, temp)

        return temp

    def run(self, state, command):
        state.foot_locations = self.step(state, command)
        return state.foot_locations

#print("OK")
