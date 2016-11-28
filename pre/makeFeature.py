from Action import *

import os

# generalize fuzzy feature for msra3d-like data file
# which means given the number of points in one frame, and the data of each points is separated in one line

def makeFeature(PATH, size_feature):
    list_dirs = os.walk(PATH)
    for root, dir, files in list_dirs:
        for f in files:
            action = Action(os.path.join(PATH, f), 20)
            features = action.calculate_fuzzy_feature()
            downsampling_features = []
            for point_features in features:
                n_of_frame = point_features.shape[0]
                epoch_size = n_of_frame // size_feature
                downsampling_result = []
                for (i, feature) in enumerate(point_features):
                    if i%epoch_size == 0 and (i//epoch_size)<size_feature:
                        downsampling_result.append(feature)
                downsampling_result = np.array(downsampling_result)
                downsampling_features.append(downsampling_result)
            downsampling_features = np.array(downsampling_features)
            #print(downsampling_features.shape)
            FEATURE_FILE_ROOT='fuzzy_features_down_sampling'
            with open(os.path.join(FEATURE_FILE_ROOT,f.split('.')[0]+'.fz'), 'w+') as wf:
                for i in downsampling_features:
                    print(i.flatten().shape)
                    for j in i.flatten():
                        print(j)
                        wf.write(str(j)+',')
                    wf.write('\n')
            wf.close()

makeFeature("../data/msra3d/", 10)
