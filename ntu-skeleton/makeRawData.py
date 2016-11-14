import numpy as np
import os

rootDir = "."

list_dirs = os.walk(rootDir)
for root, dirs, files in list_dirs:
    for filename in files:
        filepath = os.path.join(root, filename)
        makeData(filepath)
        
def makeData(filename):
    fileid = fopen(filename)