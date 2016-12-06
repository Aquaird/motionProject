import numpy as np
import matplotlib.pyplot as plt
from tfrbm import BBRBM, GBRBM
import os

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

#mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)
#mnist_image = mnist.train.images

def get_data(PATH):
    features = []
    list_dirs = os.walk(PATH)
    for root, dirs, files in list_dirs:
        for f in files:
            with open(os.path.join(PATH,f),'r') as fh:
                line = fh.readline()
                while line:
                    f_line = line.split(",")
                    #print(f_line)
                    for (i,x) in enumerate(f_line):
                        if x=='\n':
                            pass
                        else:
                            f_line[i] = float(x)
                    features.append(f_line[:-1])
                    line = fh.readline()

    features = np.array(features)
    print(features.shape)
    return features

gbrbm = GBRBM(n_visible=120, n_hidden=12, learning_rate=0.01,momentum =0.95,tqdm=None)
features = get_data("./data/fuzzy/10ds/ntu")
errs = gbrbm.fit(features, n_epoches=1000, batch_size = features.shape[0])
#cluster_result = gbrbm.transform(features)

n_of_point = 25

def data_iterator():
    generator = []
    return generator


def find_cluster(hidden_value, true_bounder):
    cluster = 0
    for (i,j) in enumerate(hidden_value):
        if j>=true_bounder:
            cluster += np.power(2,i)
    return cluster

msra_features = get_data('./data/fuzzy/10ds/ntu')
cluster_result = gbrbm.transform(msra_features)

for (i,j) in enumerate(cluster_result):
    if i%n_of_point == 0:
        print('-------------------------------------------------------')
    print(i%n_of_point+1, "->",find_cluster(j, 0.7))

