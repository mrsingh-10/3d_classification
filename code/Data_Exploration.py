import pandas as pd
import open3d as o3d
import numpy as np
import os
from pyntcloud import PyntCloud
from HelperClass import HelperClass as Helper

print(o3d.__version__)
#Open a file 
# DEMO CALLS
model = "night_stand_0030"
isTestModel = False
current_inputModel,current_outputModel = Helper.getFoldersFromModel(model,isTestModel)

# Exported VoxelGrid
voxels = Helper.importVoxelGrid(current_outputModel).get_voxels()
#maxArray = np.array([0, 0, 0],np.int32)

# creating a numpy array of 128, but we need only 101 -> + padding
array = np.zeros((128,128,128,1))
for i in range(len(voxels)): 
    x,y,z = voxels[i].grid_index
    array[x][y][z] = 1
    #maxArray = np.maximum(maxArray, voxels[i].grid_index)

# to check
for x,y,z in ((a,b,c) for a in range (101) for b in range (101) for c in range (101)):
    value = array[x][y][z]
    if value > 0 and x == 1 and y == 52 : print(x,y,z,value)
    