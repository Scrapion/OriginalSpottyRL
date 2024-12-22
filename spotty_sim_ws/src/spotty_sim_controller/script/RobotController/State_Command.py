#!/usr/bin/env python3

import numpy as np
from enum import Enum


class BehaviorState(Enum):
    REST = 0
    #Nel caso aggiungere altri stati.


class State(object):

    def __init__(self, neutral_height):
        self.velocity = np.array([0., 0.])
        self.yaw_rate = 0.

        self.robot_height = -neutral_height

        self.foot_locations = np.zeros((3, 4))

        self.body_local_position = np.array([0., 0., 0.])
        self.body_local_orientation = np.array([0., 0., 0.])

        self.imu_roll = 0.
        self.imu_pitch = 0.

        self.ticks = 0

        self.behavior_state = BehaviorState.REST


class Command(object):

    def __init__(self, neutral_height):
        self.velocity = np.array([0., 0.])
        self.yaw_rate = 0.

        self.robot_height = -neutral_height

        self.rest_event = False
