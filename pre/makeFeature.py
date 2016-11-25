from Action import *

import os

# generalize fuzzy feature for msra3d-like data file
# which means given the number of points in one frame, and the data of each points is separated in one line

def makeFeature(PATH, size_feature):
    list_dirs = os.walk(PATH)
    for root, dir, files in list_dirs:
        for f in files:
            action = Action(os.path.join(PATH, f), 20)
            fuzzy_features = action.calculate_fuzzy_feature()
            downsampling_fuzzy_features = []
            for point_features in fuzzy_features:
                n_of_frame = point_features.shape[0]
                epoch_size = n_of_frame // size_feature
                downsampling_result = []
                for (i, feature) in enumerate(point_features):
                    if i%epoch_size == 0 and (i//epoch_size)<size_feature:
                        downsampling_result.append(feature)
                downsampling_result = np.array(downsampling_result)
                downsampling_fuzzy_features.append(downsampling_result)
            downsampling_fuzzy_features = np.array(downsampling_fuzzy_features)
            #print(downsampling_fuzzy_features.shape)
            FEATURE_FILE_ROOT='fuzzy_features_down_sampling'
            with open(os.path.join(FEATURE_FILE_ROOT,f.split('.')[0]+'.fz'), 'w+') as wf:
                for i in downsampling_fuzzy_features:
                    #print(str(i.flatten())[1:-1])
                    wf.write(str(i.flatten())[1:-1]+'\n')
            wf.close()

makeFeature("../data/msra3d/", 10)
