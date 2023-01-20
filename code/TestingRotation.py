import numpy as np
from random import sample
from HelperClass import HelperClass as Helper

# DEMO CALLS
# model = "toilet_0052"
# isTestModel = False

# current_inputModel,current_outputModel = Helper.getFoldersFromModel(model,isTestModel,"Output_v3") #ROTATED_
# print(Helper.getFullPathForModel(model, isTestModel, "Test", False, suffix=""))
# voxelGrid = Helper.importVoxelGrid(current_outputModel)
# Helper.show(voxelGrid)

# def arrayOf(voxelGrid):
#     return np.array(list(map(lambda x:x.grid_index,voxelGrid.get_voxels())))

# array = [i for i in range (1,12) ]
# print(array)
# print(sample(array, 4))
# #count = [0 for _ in range (11) ]
# for number in sample(array, 3):
#     print(number)
#     rotated = Helper.getVGRotated(voxelGrid,rz=(number*2*np.pi/12))
#     Helper.createOutputFoldersForModel(model,"Output_ROTATED")
#     fileName = Helper.getFullPathForModel(model, isTestModel, "Output_ROTATED", False, suffix="_"+str(number*30))
#     Helper.exportVoxelGrid(fileName,rotated)
#     Helper.show(Helper.importVoxelGrid(fileName))

model = "bed_0516"
isTestModel = True
VOXEL_GRID_SIZE = 32

# importing
inputModelPath = Helper.getFullPathForModel(model, isTestModel, "Output_v3", isMesh=False, suffix="")
print(f"Importing {inputModelPath}")
voxelGrid = Helper.importVoxelGrid(inputModelPath)
Helper.show(voxelGrid)

# rotating to get 150°= 5*30
number = 5
rotated = Helper.getVGRotated(voxelGrid,rz=(number*2*np.pi/12), voxelGridSize=VOXEL_GRID_SIZE)
Helper.describeVoxels(rotated.get_voxels(), VOXEL_GRID_SIZE)
Helper.createOutputFoldersForModel(model,"Output_ROTATED")
fileName = Helper.getFullPathForModel(model, isTestModel, "Output_ROTATED", False, suffix="_"+str(number*30))
Helper.exportVoxelGrid(fileName,rotated)
Helper.show(Helper.importVoxelGrid(fileName))