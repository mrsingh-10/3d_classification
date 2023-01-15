import open3d as o3d
import numpy as np
from HelperClass import HelperClass as Helper
import os

print(o3d.__version__)
#Open a file 
# DEMO CALLS
model = "night_stand_0030"
isTestModel = False
VOXEL_GRID_SIZE = 64
# TODO: Helper = Helper(VOXEL_GRID_SIZE=VOXEL_GRID_SIZE)

current_inputModel,current_outputModel = Helper.getFoldersFromModel(model,isTestModel)
Helper.describeVoxels(Helper.importVoxelGrid(current_outputModel).get_voxels(),VOXEL_GRID_SIZE)


# dooing for all the models
baseDIR = os.path.dirname(__file__)
modelNetDIR = os.path.join(baseDIR,"ModelNet10")

models = ["bathtub", "bed", "chair", "desk", "dresser", "monitor", "night_stand","sofa","table", "toilet"]

for modelFolder, test in ((x, y) for x in models for y in (True,False)):
    print(f'current modelFolderName= {modelFolder} and isTestFolder={test}')
    # PRELIMINARY STEPS for getting the input folder and creating respective output folder
    
    # 1) Getting INPUT FILES
    inputDIR = os.path.join(modelNetDIR,modelFolder,"test" if test else "train")
    print(f'Working on {modelFolder} in folder {inputDIR}')
    # print(os.path.isdir(inputDIR))
    
    # Getting the list of all mesh in the directory 'modelFolder'
    inputModels = []
    # Iterate directory
    for path in os.listdir(inputDIR):
        # check if current path is an expected file
        if os.path.isfile(os.path.join(inputDIR, path)) and os.path.join(inputDIR, path).endswith(Helper.INPUT_EXTENTION):
            # append only the file name
            inputModels.append(os.path.splitext(path)[0])
    #print(inputModels)

    # 3) Voxelizing all input files
    for path in inputModels:
        current_inputModel,current_outputModel = Helper.getFoldersFromModel(path,test)
        Helper.describeVoxels(Helper.importVoxelGrid(current_outputModel).get_voxels(),VOXEL_GRID_SIZE)