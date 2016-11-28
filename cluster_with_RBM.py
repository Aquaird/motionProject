import numpy as np
import matplotlib.pyplot as plt
from tfrbm import BBRBM, GBRBM
import os

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)
mnist_image = mnist.train.images

features = []
PATH = "./pre/norm_point_down_sampling/"
list_dirs = os.walk(PATH)
for root, dirs, files in list_dirs:
    for f in files:
        with open(os.path.join(PATH,f),'r') as fh:
            line = fh.readline()
            while line:
                f_line = line.split(",")
                for (i,x) in enumerate(f_line):
                    if x=='\n':
                        pass
                    else:
                        f_line[i] = float(x)
                features.append(f_line[:-1])
                line = fh.readline()

features = np.array(features)
print(features.shape)
gbrbm = GBRBM(n_visible=30, n_hidden=3, learning_rate=0.001,momentum =0.95,tqdm=None)
errs = gbrbm.fit(features, n_epoches=1000, batch_size = 11340)
cluster_result = gbrbm.transform(features)

n_of_point = 20
def find_cluster(hidden_value, true_bounder):
    cluster = 0
    for (i,j) in enumerate(hidden_value):
        if j>=true_bounder:
            cluster += np.power(2,i)
    return cluster

for (i,j) in enumerate(cluster_result):
    if i%20 == 0:
        print('-------------------------------------------------------')
    print(find_cluster(j, 0.8))

