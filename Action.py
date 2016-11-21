import os
import numpy as np
import csv
from general import *

ROOT = 6
POINT_NUMBER = 20


# read data to form a action seq
# return pose seq(20*frame) and point seq(frame*20)
# action_seq is consisted of pose in each frame
# point_seq is consisted of each points' traj
# each point_value is norm by its root

class Action():
    def __init__(self, filename):
        self.action_seq = []
        self.point_seq = []

        self.norm_action_seq = []
        self.norm_point_seq = []
        self.maxmin_action_seq = []
        self.maxmin_point_seq = []

        self.frame_number = 0
        self.point_number = 0

        self.ROOT_INDEX = 6
        self.MEAN = []
        self.pca_vector = []

        self.bounder = [[float("inf"),float("-inf")],[float("inf"),float("-inf")],[float("inf"),float("-inf")]]#x,y,z
        self.norm_bounder = [[float("inf"),float("-inf")],[float("inf"),float("-inf")],[float("inf"),float("-inf")]] #x,y,z
        self.bounders = []
        self.norm_bounders = []

        self.filename = filename
        self.read_action()
        self.normalization()
        self.calculate_bounders()
        self.maxminnorm()

    def read_action(self):
        for i in range(0, POINT_NUMBER):
            self.point_seq.append([])
        # print(point_seq)
        with open(self.filename, 'r') as f:
            reader = f.readlines()
            i = 0
            pose = []
            for __row in reader:
                # print(__row)
                _row = __row.split(" ")
                point_data = [float(_row[0]), float(_row[1]), float(_row[2])]
                # print(point_data)
                self.point_seq[i].append(point_data)
                if (POINT_NUMBER - 1) == i:

                    #calculate mean
                    a_pose = np.array(pose)
                    mean_x = np.mean(a_pose[:,0])
                    mean_y = np.mean(a_pose[:,1])
                    mean_z = np.mean(a_pose[:,2])
                    mean_point=[mean_x, mean_y, mean_z]
                    self.MEAN.append(mean_point)

                    #calculate PCA
                    self.pca_vector.append(PCA_vector(a_pose))
                    self.action_seq.append(pose)
                    pose = []
                    i = 0
                else:
                    i += 1
                pose.append(point_data)

        self.frame_number = len(self.action_seq)
        self.point_number = len(self.point_seq)
        return [self.action_seq, self.point_seq]

    def maxminnorm(self):
        maxmin = [0.0,0.0,0.0]
        maxmin[0] = self.norm_bounder[0][1] - self.norm_bounder[0][0]
        maxmin[1] = self.norm_bounder[1][1] - self.norm_bounder[1][0]
        maxmin[2] = self.norm_bounder[2][1] - self.norm_bounder[2][0]

        for pose in self.norm_action_seq:
            maxmin_pose = []
            for joint in pose:
                maxmin_joint = [0.0,0.0,0.0]
                for axi in range(0,3):
                    maxmin_joint[axi] = (joint[axi] - self.norm_bounder[axi][0]) / maxmin[axi]

                maxmin_pose.append(maxmin_joint)
            self.maxmin_action_seq.append(maxmin_pose)

        for i in range(0, len(self.norm_point_seq)):
            self.maxmin_point_seq.append([])
        for i in range(0, len(self.norm_point_seq)):
            for j in range(0, self.frame_number):
                maxmin_joint = [0.0,0.0,0.0]
                for axi in range(0,3):
                    maxmin_joint[axi] = (self.norm_point_seq[i][j][axi] - self.norm_bounder[axi][0]) / maxmin[axi]
            self.maxmin_point_seq[i].append(maxmin_joint)
        return [self.maxmin_action_seq, self.maxmin_point_seq]



    def normalization(self):
        for i,pose in enumerate(self.action_seq):
            norm_pose = []
            for joint in pose:
                norm_joint = [0.0,0.0,0.0]
                for axi in range(0,3):
                    norm_joint[axi] = joint[axi] - self.MEAN[i][axi]
                norm_pose.append(norm_joint)
            self.norm_action_seq.append(norm_pose)

        for i in range(0, len(self.point_seq)):
            self.norm_point_seq.append([])
        for i in range(0, len(self.point_seq)):
            for j in range(0, self.frame_number):
                norm_joint = [0.0,0.0,0.0]
                for axi in range(0,3):
                    norm_joint[axi] = self.point_seq[i][j][axi] - self.MEAN[j][axi]
                self.norm_point_seq[i].append(norm_joint)
        return [self.norm_action_seq, self.norm_point_seq]

    # calculate the x,y,z bounder of data in one action_seq
    # todo calculate the bounder of each point
    def calculate_bounders(self):

        for points in self.point_seq:
            self.bounders.append(calculate_bounder(points))
        for points in self.norm_point_seq:
            self.norm_bounders.append(calculate_bounder(points))

        for i in self.bounders:
            if i[0][0] < self.bounder[0][0]:
                self.bounder[0][0] = i[0][0]
            if i[0][1] > self.bounder[0][1]:
                self.bounder[0][1] = i[0][1]
            if i[1][0] < self.bounder[1][0]:
                self.bounder[1][0] = i[1][0]
            if i[1][1] > self.bounder[1][1]:
                self.bounder[1][1] = i[1][1]
            if i[2][0] < self.bounder[2][0]:
                self.bounder[2][0] = i[2][0]
            if i[2][1] > self.bounder[2][1]:
                self.bounder[2][1] = i[2][1]

        for i in self.norm_bounders:
            if i[0][0] < self.norm_bounder[0][0]:
                self.norm_bounder[0][0] = i[0][0]
            if i[0][1] > self.norm_bounder[0][1]:
                self.norm_bounder[0][1] = i[0][1]
            if i[1][0] < self.norm_bounder[1][0]:
                self.norm_bounder[1][0] = i[1][0]
            if i[1][1] > self.norm_bounder[1][1]:
                self.norm_bounder[1][1] = i[1][1]
            if i[2][0] < self.norm_bounder[2][0]:
                self.norm_bounder[2][0] = i[2][0]
            if i[2][1] > self.norm_bounder[2][1]:
                self.norm_bounder[2][1] = i[2][1]
        return [self.bounder, self.norm_bounder]
    
a = Action("msra3d/a01_s01_e01_skeleton3D.txt")
