import sys
import os
from pathlib import Path
import time
from joblib import Parallel, delayed

# TO ADD preprocessing as module
path = Path(__file__)
while (path.stem != "code"):
    path = path.parent
sys.path.append(os.fspath(path.absolute()))

from preprocessing.HelperClass import HelperClass as Helper


# PARAMETERS
VOXEL_GRID_SIZE = 32        # L/W/H of each voxel
INPUT_EXTENTION = ".off"
OUTPUT_EXTENTION = ".ply"

def meshToVoxel(model,test):
    # IMPORT STEP
    print("Current model:", model)
    current_inputModel,current_outputModel = Helper.getFoldersFromModel(model,isTestModel=test,subFolderDirName=outputDirName)
    
    # Importing the mesh from the disk
    mesh = Helper.importMesh(current_inputModel) #.compute_vertex_normals()
    voxelGrid = Helper.getVoxelGridFromMesh(mesh,VOXEL_GRID_SIZE)
    Helper.exportVoxelGrid(current_outputModel,voxelGrid)

# DEMO CALLS
modelNetDIR = os.path.join(Helper.getInputDir(),"ModelNet10")
outputDirName = "Test"

models = ["bathtub", "bed", "chair", "desk", "dresser", "monitor", "night_stand","sofa","table", "toilet"]

#models = ["night_stand"]
#for modelFolder in models:
#    test = False
total = time.time()
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
        if os.path.isfile(os.path.join(inputDIR, path)) and os.path.join(inputDIR, path).endswith(INPUT_EXTENTION):
            # append only the file name
            inputModels.append(os.path.splitext(path)[0])
    #print(inputModels)

    # 2) Creating Output Directories
    Helper.createOutputFoldersForModelFolder(modelFolder,outputDirName)

    # 3) Voxelizing all input files
    t = time.time()
    Parallel(n_jobs=4)(delayed(meshToVoxel)(path,test) for path in inputModels) #n_jobs=-2 # use all cpu exept 1
    print("Time:",time.time() - t)
print("Total Time:",time.time() - total)