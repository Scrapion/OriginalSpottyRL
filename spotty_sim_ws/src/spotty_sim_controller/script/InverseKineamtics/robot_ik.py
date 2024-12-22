#!/usr/bin/env python3

import numpy as np
from math import sqrt, atan2, sin, cos, pi
from RoboticsUtilities.transformation import homog_transform, homog_transform_inverse


class InverseKinematics(object):

    def __init__(self, body_dimension, leg_dimension):
        self.body_length = body_dimension[0]
        self.body_width = body_dimension[1]

        self.l1 = leg_dimension[0]
        self.l2 = leg_dimension[1]
        self.l3 = leg_dimension[2]
        self.l4 = leg_dimension[3]

    def get_local_position(self, leg_position, dx, dy, dz, roll, pitch, yaw):
        leg_position = (np.block([[leg_position], [np.array([1, 1, 1, 1])]])).T

        # Transformation matrix, base_link_world => base_link
        T_base_link_world_base_link = homog_transform(dx, dy, dz, roll, pitch, yaw)

        # Transformation matrix, base_link_world => front_right_leg
        T_base_link_world_fr = np.dot(T_base_link_world_base_link, homog_transform(0.5 * self.body_length,
                                                                                   -0.5 * self.body_width,
                                                                                   0, pi / 2, -pi / 2, 0))

        # Transformation matrix, base_link_world => front_left_leg
        T_base_link_world_fl = np.dot(T_base_link_world_base_link, homog_transform(0.5 * self.body_length,
                                                                                   0.5 * self.body_width,
                                                                                   0, pi / 2, -pi / 2, 0))

        # Transformation matrix, base_link_world => rear_right_leg
        T_base_link_world_rr = np.dot(T_base_link_world_base_link, homog_transform(-0.5 * self.body_length,
                                                                                   -0.5 * self.body_width,
                                                                                   0, pi / 2, -pi / 2, 0))

        # Transformation matrix, base_link_world => rear_left_leg
        T_base_link_world_rl = np.dot(T_base_link_world_base_link, homog_transform(-0.5 * self.body_length,
                                                                                   0.5 * self.body_width,
                                                                                   0, pi / 2, -pi / 2, 0))

        # Coordinate locali

        pos_FR = np.dot(homog_transform_inverse(T_base_link_world_fr), leg_position[0])
        pos_FL = np.dot(homog_transform_inverse(T_base_link_world_fl), leg_position[1])
        pos_RR = np.dot(homog_transform_inverse(T_base_link_world_rr), leg_position[2])
        pos_RL = np.dot(homog_transform_inverse(T_base_link_world_rl), leg_position[3])

        return np.array([pos_FR[:3], pos_FL[:3], pos_RR[:3], pos_RL[:3]])

    def inverse_kinematics(self, leg_position, dx, dy, dz, roll, pitch, yaw):
        """
        Calcola la cinematica inversa per tutte le gambe del robot
        """

        position = self.get_local_position(leg_position, dx, dy, dz, roll, pitch, yaw)

        angles = []

        for i in range(4):
            x = position[i][0]
            y = position[i][1]
            z = position[i][2]

            F = sqrt(x ** 2 + y ** 2 - self.l2 ** 2)
            G = F - self.l1
            H = sqrt(G ** 2 + z ** 2)

            theta1 = -atan2(y, x) - atan2(F, self.l2 * (-1) ** i)

            D = (H ** 2 - self.l3 ** 2 - self.l4 ** 2) / (2 * self.l3 * self.l4)

            theta4 = -atan2((sqrt(1 - D ** 2)), D)

            theta3 = atan2(z, G) - atan2(self.l4 * sin(theta4), self.l3 + self.l4 * cos(theta4))

            angles.append(theta1)
            angles.append(theta3)
            angles.append(theta4)

        return angles


#print("OK")
