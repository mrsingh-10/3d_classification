# TO ADD preprocessing as module
import sys
import os
from pathlib import Path

path = Path(__file__)
while (path.stem != "code"):
    path = path.parent
sys.path.append(os.fspath(path.absolute()))

from preprocessing.HelperClass import HelperClass as Helper
# TO ADD preprocessing as module

import time
from random import shuffle
import numpy as np


# PARAMETERS
VOXEL_GRID_SIZE = 32        # L/W/H of each voxel


# folders&files setting
INPUT_EXTENTION = ".ply"
OUTPUT_EXTENTION = ".ply"

inputDirName = "Output_v3"
inputDirPath = os.path.join(Helper.getOutputDir(), inputDirName)

outputDirName = "Output_subset_v1"

# which set to export
TRAIN_SET = False
TEST_SET = True
TOT_SAMPLES = 20

# which categories to export
models = ["bathtub", 
          "bed", "chair", "desk", "dresser","monitor", "night_stand", "sofa", "table", "toilet"]

def arrayOf(voxelGrid):
    return np.array(list(map(lambda x: x.grid_index, voxelGrid.get_voxels())))


def export(model, isTestModel):
    # IMPORT STEP
    print("Copying Current model:", model)
    importFileName = Helper.getFullPathForModel(model, isTestModel, inputDirName, isMesh=False)
    exportFileName = Helper.getFullPathForModel(model, isTestModel, outputDirName, isMesh=False) #os.path.dirname()
    print("IN:",importFileName,"\nOUT:",exportFileName)
    os.popen(f'copy {importFileName} {exportFileName}')


total = time.time()
def eportSubset(folders, subsetSize = TOT_SAMPLES):
    for modelFolder, test in ((x, y) for x in folders for y in (True, False)):
        # TODO change this is temporary solution
        if (not TEST_SET) and test: 
            print("skipING TEST:",(not TEST_SET and test),test)
            continue
        if (not TRAIN_SET) and not test: 
            print("skipING TRAIN:",(not TRAIN_SET and test),test)
            continue

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
        for path in inputModels[:subsetSize]:
            export(path, test)
        print("Time:", time.time() - t)
    print("Total Time:", time.time() - total)

eportSubset(models)
print()
