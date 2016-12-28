from Action import *

import os
from joblib import Parallel, delayed

# generalize fuzzy feature for msra3d-like data file
# which means given the number of points in one frame, and the data of each points is separated in one line

def makeFeature(PATH, out_path, point_number,size_feature,fz=True):
    action = Action(PATH, point_number)
    if fz:
        features = action.calculate_fuzzy_feature()
    else:
        features = np.array(action.norm_point_seq)
    downsampling_features = []
    fileName = PATH.split('.')[-2].split('/')[-1]
    # in every point seq:
    for point_features in features:
        n_of_frame = point_features.shape[0]
        epoch_size = n_of_frame // size_feature
        if(0 == epoch_size):
            continue
        downsampling_result = []
        #in every frame of a point seq:
        for (i, feature) in enumerate(point_features):
            #if this frame is needed to be sampled
            if i%epoch_size == 0 and (i//epoch_size)<size_feature:
                downsampling_result.append(feature)
            #downsampling_result = np.array(downsampling_result)
        downsampling_features.append(np.array(downsampling_result))

    a_downsampling_features = np.array(downsampling_features)
    #print(a_downsampling_features.shape)
    #print(os.path.join(out_path,PATH.split('.')[0]+'.fz'))
    if fz:
        app = '.fz'
    else:
        app = '.ft'
    with open(os.path.join(out_path,fileName+app), 'w+') as wf:
        for i in a_downsampling_features:
            print(i.flatten().shape)
            for j in i.flatten():
                wf.write(str(j)+',')
            wf.write('\n')
    wf.close()

if __name__ == '__main__':
    rawdata_root = '../data/ntu_all'
    feature_root = '../data/fuzzy/10ds/ntu_all'
    point_number = 25
    size_feature = 10
    for root,dirs,files in os.walk(rawdata_root):
        Parallel(n_jobs=12)(delayed(makeFeature)(os.path.join(rawdata_root, fileName), feature_root, point_number,size_feature,fz=True) for fileName in sorted(files))
