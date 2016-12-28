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

def train_model(model, inputData, savePath, dataSize, hiddenSize, rate, mom, ne):
        #saver = tf.train.Saver()
    #s = saver.save(gbrbm.sess, save_path+".ckpt")
    gbrbm.save_weights(save_path+".ckpt", path_list[0]+'_'+path_list[1]+'_'+path_list[2])
    print("Model saved in file: %s", save_path)
    return gbrbm
#cluster_result = gbrbm.transform(features)

'''
def data_iterator():
    generator = []
    return generator
'''

def find_cluster(hidden_value, true_bounder):
    cluster = 0
    for (i,j) in enumerate(hidden_value):
        if j>=true_bounder:
            cluster += np.power(2,i)
    return cluster

def test_cluster(test_data, point_number, gbrbm):
    data = get_data(test_data)
    cluster_result = gbrbm.transform(data)
    for (i,j) in enumerate(cluster_result):
        if i%n_of_point == 0:
            print('-------------------------------------------------------')
        print(i%n_of_point+1, "->",find_cluster(j, 0.7))


dataSize = 240
hiddenSize = 30
rate = 0.0001
mom = 0.95
ne = 1000

gbrbm = GBRBM(n_visible=dataSize, n_hidden=hiddenSize, learning_rate=rate,momentum =mom,tqdm=None)

#
#baseName = "fuzzy/10ds/msra3d"
#features = get_data(os.path.join("./data", baseName))
#errs = gbrbm.fit(features, n_epoches=ne, batch_size = features.shape[0])

baseName = "fuzzy/10ds/ntu_all"
features = get_data(os.path.join("./data", baseName))
errs = gbrbm.fit(features, n_epoches=ne, batch_size = round(features.shape[0]/100))

path_list = baseName.split('/')
save_path = os.path.join("./trained", path_list[0]+'_'+path_list[1]+'_'+path_list[2])

n_of_point = 25
test_path = './data/fuzzy/10ds/ntu'
test_cluster(test_path, n_of_point, gbrbm)
