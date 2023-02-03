import numpy as np
from HelperClass import HelperClass as Helper
from random import sample
from random import shuffle
import time
from joblib import Parallel, delayed
import os

# PARAMETERS
VOXEL_GRID_SIZE = 32        # L/W/H of each voxel


# folders&files setting
INPUT_EXTENTION = ".ply"
OUTPUT_EXTENTION = ".ply"
baseDIR = os.path.dirname(__file__)
inputDirPath = os.path.join(baseDIR, "Output_v3")

inputDirName = "Output_v3"
outputDirName = "Output_ROTATED_v7"

# which set to export
TRAIN_SET = False
TEST_SET = True

ROTATIONS = 3

# which categories to export
models = ["bathtub", "bed", "chair", "desk", "dresser",
          "monitor", "night_stand", "sofa", "table", "toilet"]

models_2 = ["bed", "chair", "monitor", "sofa"] # x2
models_3 = ["table", "toilet"] # x3
models_5 = ["desk", "dresser", "night_stand"] # x5
models_8 = ["bathtub"] # x8



def arrayOf(voxelGrid):
    return np.array(list(map(lambda x: x.grid_index, voxelGrid.get_voxels())))

# DEMO CALLS
# model = "toilet_0052"
# isTestModel = False

# filename = Helper.getFullPathForModel(model, isTestModel, "Output_v3", isMesh=False)
# voxelGrid = Helper.importVoxelGrid(filename)
# Helper.show(voxelGrid)


# main code:
randomsGlobal = [0 for _ in range(0, 12)]
sectors = [i for i in range(0, 12)]
print(sectors)


randoms = [0 for _ in range(0, 12)]

def exportRotated(model, isTestModel, rotations = ROTATIONS):
    # IMPORT STEP
    print("Current model:", model)
    importFileName = Helper.getFullPathForModel(model, isTestModel, inputDirName, isMesh=False)
    voxelGrid = Helper.importVoxelGrid(importFileName)

    # Get 3 different rotations and export
    for number in sample(sectors, rotations):
        # print(number)
        randoms[number] += 1
        randomsGlobal[number] += 1
        rotated = Helper.getVGRotated(
            voxelGrid, voxelGridSize=VOXEL_GRID_SIZE, rz=(number*2*np.pi/12))
        exportFileName = Helper.getFullPathForModel(
            model, isTestModel, outputDirName, isMesh=False, suffix="_"+str(number*30))
        print("Exporting", model+"_"+str(number*30))
        Helper.exportVoxelGrid(exportFileName, rotated)


total = time.time()
def tempSol(folders,rotations):
    for modelFolder, test in ((x, y) for x in folders for y in (True, False)):
        # TODO change this is temporary solution
        if (not TEST_SET) and test: 
            print("skipING TEST:",(not TEST_SET and test),test)
            continue
        if (not TRAIN_SET) and not test: 
            print("skipING TRAIN:",(not TEST_SET and test),test)
            continue

        randoms = [0 for _ in range(0, 12)]
        # print(f'current modelFolderName= {modelFolder} and isTestFolder={test}')
        # PRELIMINARY STEPS for getting the input folder and creating respective output folder

        # 1) Getting INPUT FILES
        inputDIR = os.path.join(inputDirPath, modelFolder,
                                "test" if test else "train")
        # print(f'Working on {modelFolder} in folder {inputDIR}')
        # print(os.path.isdir(inputDIR))

        # Getting the list of all mesh in the directory 'modelFolder'
        inputModels = []
        # Iterate directory
        for path in os.listdir(inputDIR):
            # check if current path is an expected file
            if os.path.isfile(os.path.join(inputDIR, path)) and os.path.join(inputDIR, path).endswith(INPUT_EXTENTION):
                # append only the file name
                inputModels.append(os.path.splitext(path)[0])
        print(f'{modelFolder}/{"test" if test else "train"} has {len(inputModels)} models')

        # 2) Creating Output Directories
        Helper.createOutputFoldersForModelFolder(modelFolder, outputDirName)

        # 3) Voxelizing all input files
        # NEW:
        # print("before:", inputModels[:10])
        shuffle(inputModels)
        # print("after:", inputModels[:10])

        t = time.time()
        for path in inputModels[:500]:
            exportRotated(path, test,rotations)
        # Parallel(n_jobs=4)(delayed(exportRotated)(path,test) for path in inputModels) #n_jobs=-2 # use all cpu exept 1
        print(f"Randoms: {randoms}")
        print("Time:", time.time() - t)
    print("Total Time:", time.time() - total)

    print(f"Randoms: {randomsGlobal}")

# tempSol(models_2,2)# = ["bed", "chair", "monitor", "sofa"] # x2
# tempSol(models_3,3)# = ["table", "toilet"] # x3
# tempSol(models_5,5)# = ["desk", "dresser", "night_stand"] # x5
# tempSol(models_8,8)# = ["bathtub"] # x8
tempSol(models,3)