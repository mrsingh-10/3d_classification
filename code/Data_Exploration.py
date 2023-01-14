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
myDic = {}

array = np.zeros((101,101,101,1))
for i in range(len(voxels)): 
    key = str(voxels[i].grid_index)
    alreadyPresent = myDic.keys().__contains__(key)
    if(alreadyPresent):
        print(voxels[i].grid_index, myDic[key],i)
    else:
        myDic[key] = i
        #print(key)
    x,y,z = voxels[i].grid_index
    array[x][y][z] += 1

    #maxArray = np.maximum(maxArray, voxels[i].grid_index)
for x,y,z in ((a,b,c) for a in range (101) for b in range (101) for c in range (101)):
    value = array[x][y][z]
    if value > 0 and x == 1 and y == 52 : print(x,y,z,value)
    

# pcl = o3d.geometry.PointCloud()
# rnd = np.random.rand(100, 3)
# pcl.points = o3d.utility.Vector3dVector(rnd)
# o3d.visualization.draw_geometries([pcl])
#print(array[1][52][97])
#print(maxArray)wq