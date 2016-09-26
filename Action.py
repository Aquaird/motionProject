import os
import numpy
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
		self.frame_number = 0
		self.point_number = 0
		self.ROOT_INDEX = 6
		self.ROOT = []
		self.MEAN = []
		self.x_bounder = [0.0, 0.0]
		self.y_bounder = [0.0, 0.0]
		self.z_bounder = [0.0, 0.0]
		self.points_bounder = []
		self.filename = filename
		temp = self.read_action()

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
					# norm
					for joint in pose:
						for axi in range(0, 3):
							joint[axi] -= pose[ROOT][axi]
					self.action_seq.append(pose)
					pose = []
					i = 0
				else:
					i += 1
				pose.append(point_data)

		# norm point_seq
		for index_of_point in range(0, len(self.point_seq)):
			for index_of_frame in range(0, len(self.point_seq[index_of_point])):
				for axi in range(0, 3):
					self.point_seq[index_of_point][index_of_frame][axi] -= self.point_seq[ROOT][index_of_frame][axi]
		self.frame_number = len(self.action_seq)
		self.point_number = len(self.point_seq)
		return [self.action_seq, self.point_seq]

	def normalization(self):
		return [self.action_seq, self.point_seq]

	# calculate the x,y,z bounder of data in one action_seq
	# todo calculate the bounder of each point
	def calculate_bounder(self):
		for action in self.action_seq:
			for point in action:
				x_value = point[0]
				y_value = point[1]
				z_value = point[2]
				if x_value < self.x_bounder[0]:
					self.x_bounder[0] = x_value
				if x_value > self.x_bounder[1]:
					self.x_bounder[1] = x_value
				if y_value < self.y_bounder[0]:
					self.y_bounder[0] = y_value
				if y_value > self.y_bounder[1]:
					self.y_bounder[1] = y_value
				if z_value < self.y_bounder[0]:
					self.z_bounder[0] = z_value
				if z_value > self.y_bounder[1]:
					self.z_bounder[1] = z_value

	# todo calculate