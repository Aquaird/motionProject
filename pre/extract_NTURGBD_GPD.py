import os
import h5py
import numpy as np
from scipy.spatial.distance import pdist
from joblib import Parallel, delayed
from sklearn.preprocessing import normalize
# version for GPD


def read_skeleton_file(file_path):
    skeleton_file = open(file_path)
    lines = skeleton_file.readlines()
    frame_count = int(lines[0])
    positions = {}
    starts = {}
    ends = {}
    ind = 1
    for f in range(0, frame_count):
        body_count = int(lines[ind])
        ind = ind + 1
        for b in range(0, body_count):
            body_id = lines[ind].split(' ')[0]
            trackingState = lines[ind].split(' ')[9]

            if body_id not in positions:
                starts[body_id] = f

                positions[body_id] = np.zeros((frame_count, 25, 3))
            joint_count = int(lines[ind + 1])
            ind = ind + 2
            for j in range(0, joint_count):
                line = lines[ind + j]
                positions[body_id][f, j] = [
                    float(w) for w in line.split(' ')[0:3]]
            ends[body_id] = f
            ind = ind + joint_count

    body_var = {}

    if bool(positions):
        for key, value in positions.items():
            # if frame_count != len(np.trim_zeros(value[:, 1, 0])):
            # print file, key, frame_count, len(np.trim_zeros(value[:, 1, 0]))
            body_var[key] = 0
            for j in range(0, 25):
                body_var[key] += np.var(value[starts[key]:ends[key], j, 0]) + \
                    np.var(value[starts[key]:ends[key], j, 1]) + \
                    np.var(value[starts[key]:ends[key], j, 2])
        import operator
        chosen_body_id = max(body_var.items(),
                             key=operator.itemgetter(1))[0]
        pos = positions[chosen_body_id]
        start = starts[chosen_body_id]
        end = ends[chosen_body_id] + 1
        return pos[start:end], start, end, frame_count, chosen_body_id
    else:
        return None, None, None, frame_count, None


def writeIntoFile(input_name, output_root, input_root):
    basename = input_name.split('.')[0]
    f = open(os.path.join(data_root, basename+'.skeleton'), 'w')
    file_path = os.path.join(input_root, input_name)
    pos, start, end, frame_count, body_id = read_skeleton_file(file_path)

    a_pos = np.array(pos)
    print(frame_count, start, end, body_id, a_pos.shape)
    if body_id is None:
        return
    else:
        for n_o_f in range(0, end-start):
            for n_o_j in range(0, len(a_pos[n_o_f])):
                #print(a_pos[n_o_f][n_o_j])
                for i in a_pos[n_o_f][n_o_j]:
                    f.write(str(i)+' ')
                f.write('\n')


if __name__ == '__main__':

    skeleton_root = '/home/lym/motionData/AllSkeletonFiles_remove_nan_nolabel'
    data_root = '../data/ntu'

    for root, dirs, files in os.walk(skeleton_root):
        Parallel(n_jobs=24)(delayed(writeIntoFile)(fileName, data_root, skeleton_root) for fileName in sorted(files))
