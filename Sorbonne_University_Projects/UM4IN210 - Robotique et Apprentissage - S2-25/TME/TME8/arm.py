#################################################################################################
#                                                                                               #
#                                                                                               #
#                Evolutionary playground: from convergent to divergent search                   #
#                                                                                               #
#                                                                                               #
#################################################################################################
#                                                                                               #
#                                                                                               #
#   Copyright (C) 2020 Stephane Doncieux, Sorbonne Université                                   #
#                                                                                               #
#  This program is free software; you can redistribute it and/or modify it under the terms      #
#  of the GNU General Public License as published by the Free Software Foundation;              #
#  either version 2 of the License, or (at your option) any later version.                      #
#                                                                                               #
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;    #
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    #
#  See the GNU General Public License for more details.                                         #
#                                                                                               #
#  You should have received a copy of the GNU General Public License along with this program;   #
#  if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330,             #
#  Boston, MA 02111-1307 USA                                                                    #
#                                                                                               #
#                                                                                               #
#################################################################################################
#                                                                                               #
# This code allows to run different variants of gradient free direct policy search algorithms   #
# It relies on the DEAP framework to allow an easy exploration of EA components (selection,     #
# mutation, ...), see https://deap.readthedocs.io for more details.                             #
#                                                                                               #
# To use it, set the env_name variable below and launch it with python:                                                        #
#       python3 ea_dps.py                                                                        #
#                                                                                               #
# If you have multiple cores on your computer, consider using scoop, it will parallelize        #
# the run and thus greatly accelerate it:                                                       #
#       python3 -m scoop ea_dps.py                                                               #
#                                                                                               #
#################################################################################################
import numpy as np
from math import pi, cos, sin
from matplotlib import pyplot as plt
import matplotlib.cm as cm

# Computing segment intersection (from https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/)


def ccw(A, B, C):
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


class Arm:
    def __init__(self, lengths, obstacle_position, target_position, walls=[]):
        self.n_dofs = len(lengths)
        self.lengths = np.concatenate(([0], lengths))
        self.obstacle_position = obstacle_position
        self.target_position = target_position
        self.walls = walls

        # Initialize default values
        self.joint_xy = []
        self.angles = np.zeros(self.n_dofs)
        self.angles_velocity = np.zeros(self.n_dofs)
        self.angle_acceleration = 0.1

    def fw_kinematics(self, p):
        assert (len(p) == self.n_dofs)
        p = np.append(p, 0)
        self.joint_xy = []
        mat = np.matrix(np.identity(4))
        for i in range(0, self.n_dofs + 1):
            m = [[cos(p[i]), -sin(p[i]), 0, self.lengths[i]],
                 [sin(p[i]),  cos(p[i]), 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]]
            mat = mat * np.matrix(m)
            v = mat * np.matrix([0, 0, 0, 1]).transpose()
            self.joint_xy += [v[0:2].A.flatten()]
        inters = False
        for ip in range(len(self.joint_xy)-1):
            for iw in range(len(self.walls)):
                inters = intersect(
                    self.joint_xy[ip], self.joint_xy[ip+1], self.walls[iw][0], self.walls[iw][1])
                if inters:
                    break
            if inters:
                break
        return self.joint_xy[self.n_dofs], self.joint_xy, inters

    def reset(self):
        self.angles = np.zeros(self.n_dofs)
        self.angles_velocity = np.zeros(self.n_dofs)
        end_effector_xy, joint_xy, inters = self.fw_kinematics(self.angles)
        state = np.concatenate([self.angles, self.angles_velocity])
        distance_to_target = np.linalg.norm(
            end_effector_xy - np.array(self.target_position))
        distance_to_obstacle = np.linalg.norm(
            end_effector_xy - np.array(self.obstacle_position))
        return (state, joint_xy, (distance_to_target, distance_to_obstacle), inters)

    def step(self, a):
        a = np.array(a)
        self.angles_velocity *= 0.9  # Friction
        self.angles_velocity += self.angle_acceleration * a
        self.angles += self.angles_velocity

        end_effector_xy, joint_xy, inters = self.fw_kinematics(self.angles)
        state = np.concatenate([self.angles, self.angles_velocity])
        distance_to_target = np.linalg.norm(
            end_effector_xy - np.array(self.target_position))
        distance_to_obstacle = np.linalg.norm(
            end_effector_xy - np.array(self.obstacle_position))
        return (state, joint_xy, (distance_to_target, distance_to_obstacle), inters)

    def display_trajectory(self, traj):
        cmap = cm.get_cmap('Greys')
        fig, ax = plt.subplots()
        ax.set_xlim(-np.sum(self.lengths), np.sum(self.lengths))
        ax.set_ylim(-np.sum(self.lengths), np.sum(self.lengths))

        T, N, _ = traj.shape

        for t in range(T):
            plt.plot(traj[t, :, 0], traj[t, :, 1], '-o', c=cmap(t/(T-1)))

        plt.scatter(
            self.obstacle_position[0], self.obstacle_position[1], marker='x', s=100, c='red')
        plt.scatter(
            self.target_position[0], self.target_position[1], marker='x', s=100, c='green')

        plt.axis('equal')
        plt.show()


def eval_ka(angles, lengths, target_pos, walls, resdir=None, render=False, dump=False, name=""):
    a = Arm(lengths, walls)
    v, _, inters = a.fw_kinematics(angles)
    dist_ee = -np.linalg.norm(v-target_pos)
    if inters:
        dist_ee = -1000000
        v = [0, 0]
    log = {
        "pos_end_effector": v,
        "dist_end_effector": dist_ee,
        "collision": inters
    }
    return dist_ee, v, log
