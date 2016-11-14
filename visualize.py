"""
visualize the pre-process of a action
"""

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

import Action

FILENAME = "msra3d/a01_s01_e01_skeleton3D.txt"
action = Action(FILENAME)

def visualize(action):
    