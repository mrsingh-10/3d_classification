# TO ADD preprocessing as module
import sys
import os
from pathlib import Path
from tqdm import tqdm

path = Path(__file__)
while (path.stem != "code"):
    path = path.parent
sys.path.append(os.fspath(path.absolute()))

from preprocessing.HelperClass import HelperClass as Helper
# TO ADD preprocessing as module

import time


# PARAMETERS
# folders&files setting
INPUT_EXTENTION = ".ply"

inputDirName = "Output_ROTATED_v7"
ROTATED_INPUTS = True
inputDirPath = os.path.join(Helper.getOutputDir(), inputDirName)

outputDirName = "Output_PARTITIONED_v1"
PARTITION = True # if True it will create TOT_PARTITIONS without repetitions
                  # if False it will create TOT_SUBSETS with 2x repeted

#                   if false:
# subset 1: [  1,  2,  3,  4,  5 | 10, 15, 20, 25 | 24] 5x1,  2,   3,   4, 2x5
# subset 2: [  6,  7,  8,  9, 10 |  1, 11, 16, 21 |  5] 2x1, 5x2,  3,   4,   5
# subset 3: [ 11, 12, 13, 14, 15 |  2,  7, 17, 22 |  6]   1, 2x2, 5x3,  4,   5
# subset 4: [ 16, 17, 18, 19, 20 |  3,  8, 13, 23 | 12]   1,   2, 2x3, 5x4,  5
# subset 5: [ 21, 22, 23, 24, 25 |  4,  9, 14, 19 | 18]   1,   2,   3, 2x4, 5x5

TRAIN_SET = True
TEST_SET = True
TOT_PARTITIONS = 25
TOT_SUBSETS = 5

PRINT = False

# which categories to export
models = ["bathtub", 
          "bed", "chair", "desk", "dresser","monitor", "night_stand", "sofa", "table", "toilet"]

def export(model, isTestModel, subsetId):
    # IMPORT STEP
    if PRINT: print("Copying Current model:", model)
    importFileName = Helper.getFullPathForModel(model, isTestModel, inputDirName, isMesh=False, hasRotaions=ROTATED_INPUTS)
    exportFileName = Helper.getFullPathForModel(model, isTestModel, outputDirName+"\\"+str(subsetId), isMesh=False, hasRotaions=ROTATED_INPUTS) #os.path.dirname()
    if PRINT: print("IN:",importFileName,"\nOUT:",exportFileName)
    os.popen(f'copy {importFileName} {exportFileName}')


total = time.time()
# TODO: RENAME:
def exportPartitions():
    ziped = ((x, y) for x in models for y in (True, False))
    iterator = tqdm(ziped,total=len(models*2))
    for modelFolder, test in iterator:
        # TODO change this is temporary solution
        if (not TEST_SET) and test: 
            if PRINT: print("skipING TEST:",(not TEST_SET and test),test)
            continue
        if (not TRAIN_SET) and not test: 
            if PRINT: print("skipING TRAIN:",(not TRAIN_SET and test),test)
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
        if PRINT: print(f'{modelFolder}/{"test" if test else "train"} has {len(inputModels)} models')

        # 2) Creating Output Directories
        totSubFolders = TOT_PARTITIONS if PARTITION else TOT_SUBSETS
        for i in range(totSubFolders):
            Helper.createOutputFoldersForModelFolder(modelFolder, outputDirName+"\\"+str(i+1))

        # 3) Shuffle
        # print("before:", inputModels[:10])
        # shuffle(inputModels)
        # print("after:", inputModels[:10])

        t = time.time()
        iterator2 = tqdm(enumerate(inputModels))
        for i,path in iterator2:
            iterator.set_postfix({'inner': i+1})
            partitionID = (i%TOT_PARTITIONS)+1
            # FOR PARTITION:
            # export(path, test, partitionID)

            # FOR SUBSET:
            subsetIDX1 = int((partitionID-1)/TOT_SUBSETS) % TOT_SUBSETS
            subsetIDX2 = (partitionID)%TOT_SUBSETS
            subsetIDX3 = (partitionID+1)%TOT_SUBSETS
            export(path,test, subsetIDX1+1)
            if subsetIDX1 != subsetIDX2:
                export(path,test, subsetIDX2+1)
            else:
                export(path,test, subsetIDX3+1)
        if PRINT: print("Time:", time.time() - t)
    if PRINT: print("Total Time:", time.time() - total)

# subset 1: [  1,  2,  3,  4,  5 | 6, 11, 16, 21 | 10] 5x1, 2x2,   3,   4,   5
# subset 2: [  6,  7,  8,  9, 10 | 1, 12, 17, 22 | 15]   1, 5x2, 2x3,   4,   5
# subset 3: [ 11, 12, 13, 14, 15 | 2,  7, 18, 23 | 20]   1,   2, 5x3, 2x4,   5
# subset 4: [ 16, 17, 18, 19, 20 | 3,  8, 13, 24 | 25]   1,   2,   3, 5x4, 2x5
# subset 5: [ 21, 22, 23, 24, 25 | 4,  9, 14, 19 |  5] 2x1,   2,   3,   4, 5x5



exportPartitions()