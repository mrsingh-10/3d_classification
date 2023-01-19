import numpy as np
from HelperClass import HelperClass as Helper
from random import sample
import time
from joblib import Parallel, delayed
import os

def arrayOf(voxelGrid):
    return np.array(list(map(lambda x:x.grid_index,voxelGrid.get_voxels())))
# DEMO CALLS
#model = "toilet_0052"
#isTestModel = False

#filename = Helper.getFolderFromModel(model, isTestModel, "Output_v3", isMesh=False)
#voxelGrid = Helper.importVoxelGrid(filename)
#Helper.show(voxelGrid)


# main code:

sectors = [i for i in range (1,12) ]
print(sectors)

def exportRotated(model,isTestModel):
    # IMPORT STEP
    print("Current model:", model)
    filename = Helper.getFolderFromModel(model, isTestModel, "Output_v3", isMesh=False)
    voxelGrid = Helper.importVoxelGrid(filename)
    
    # Get 3 different rotations and export
    for number in sample(sectors, 3):
        rotated = Helper.getVGRotated(voxelGrid,rz=(number*2*np.pi/12))
        fileName = Helper.getFolderFromModel(path, isTestModel, outputDirName, isMesh=False, suffix="_"+str(number*30))
        Helper.exportVoxelGrid(fileName,rotated)

models = ["bathtub", "bed", "chair", "desk", "dresser", "monitor", "night_stand","sofa","table", "toilet"]

models = ["bathtub"]
#for modelFolder in models:
#    test = False

baseDIR = os.path.dirname(__file__)
inputDirName = os.path.join(baseDIR,"Output_v3")
INPUT_EXTENTION = ".ply"
OUTPUT_EXTENTION = ".ply"

outputDirName = "Output_ROTATED"

total = time.time()
for modelFolder, test in ((x, y) for x in models for y in (True,False)):
    print(f'current modelFolderName= {modelFolder} and isTestFolder={test}')
    # PRELIMINARY STEPS for getting the input folder and creating respective output folder
    
    # 1) Getting INPUT FILES
    inputDIR = os.path.join(inputDirName,modelFolder,"test" if test else "train")
    print(f'Working on {modelFolder} in folder {inputDIR}')
    # print(os.path.isdir(inputDIR))
    
    # Getting the list of all mesh in the directory 'modelFolder'
    inputModels = []
    # Iterate directory
    for path in os.listdir(inputDIR):
        # check if current path is an expected file
        if os.path.isfile(os.path.join(inputDIR, path)) and os.path.join(inputDIR, path).endswith(INPUT_EXTENTION):
            # append only the file name
            inputModels.append(os.path.splitext(path)[0])
    #print(inputModels)

    # 2) Creating Output Directories
    Helper.createOutputFoldersForModelFolder(modelFolder,outputDirName)

    # 3) Voxelizing all input files
    t = time.time()
    Parallel(n_jobs=4)(delayed(exportRotated)(path,test) for path in inputModels) #n_jobs=-2 # use all cpu exept 1

    print("Time:",time.time() - t)
print("Total Time:",time.time() - total)