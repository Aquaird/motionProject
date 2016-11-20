import os
import numpy
import csv

# calculate the var in one seq with window_size
def calculate_var(point_seq, window_size):
    point_var = []
    window_var = []
    window = []
    for index_of_point in range(0, 20):
        point_var.append([])
    for index_of_frame in range(0, round(len(point_seq[0]) / window_size)):
        window_var.append([])

    for index_of_point in range(0, len(point_seq)):
        point_data = point_seq[index_of_point]
        for index_of_frame in range(0, len(point_data)):
            if index_of_frame != 0 and index_of_frame % window_size == 0:
                var = numpy.var(window)
                # print(window, var)
                point_var[index_of_point].append(var)
                window_var[round(index_of_frame / window_size) - 1].append(var)
                window = []
            window.append(point_data[index_of_frame])
    return [point_var, window_var]


# smooth the sequence with (-3,12,17,12,-3)/3
def savitzky_filter(sequence):
    num_element = len(sequence)
    temp_seq = []
    for i in range(0, num_element):
        if (i < 2 or i + 2 >= num_element):
            temp = sequence[i]
        else:
            temp = sequence[i]
            for j in range(len(temp)):
                temp[j] = -3.0 / 35 * (sequence[i - 2][j] + sequence[i + 2][j]) + 12.0 / 35 * (
                sequence[i - 1][j] + sequence[i + 1][j]) + 17.0 / 35 * sequence[i][j]
        temp_seq.append(temp)
    for i in range(0, num_element):
        sequence[i] = temp_seq[i]
    return sequence

def calculate_bounder(sequence):
    bounder = [[float("inf"),float("-inf")],[float("inf"),float("-inf")],[float("inf"),float("-inf")]]
    count = len(sequence)
    for i in sequence:
        x_value = i[0]
        y_value = i[1]
        z_value = i[2]
        if x_value < bounder[0][0]:
            bounder[0][0] = x_value
        if x_value > bounder[0][1]:
            bounder[0][1] = x_value
        if y_value < bounder[1][0]:
            bounder[1][0] = y_value
        if y_value > bounder[1][1]:
            bounder[1][1] = y_value
        if z_value < bounder[2][0]:
            bounder[2][0] = z_value
        if z_value > bounder[2][1]:
            bounder[2][1] = z_value
    return bounder
