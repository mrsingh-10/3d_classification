import open3d as o3d
from HelperClass import HelperClass as Helper
import os

print(o3d.__version__)
# Open a file
# DEMO CALLS
model = "bed_0516"
isTestModel = True
VOXEL_GRID_SIZE = 32
outputFolderName = "Output_ROTATED_v2"
# TODO: Helper = Helper(VOXEL_GRID_SIZE=VOXEL_GRID_SIZE)

filename = Helper.getFullPathForModel(
    model, isTestModel, outputFolderName, isMesh=False, suffix="_240")
voxelGrid = Helper.importVoxelGrid(filename)
Helper.show(voxelGrid)
Helper.describeVoxels(voxelGrid.get_voxels(), VOXEL_GRID_SIZE)


def forEach(doThis):
    # dooing for all the models
    baseDIR = os.path.dirname(__file__)
    rootModelsDirName = os.path.join(baseDIR, outputFolderName)

    models = ["bathtub", "bed", "chair", "desk", "dresser",
              "monitor", "night_stand", "sofa", "table", "toilet"]
    models = ["bed"]

    for modelFolder, isTestModel in ((x, y) for x in models for y in (True, False)):
        print(
            f'current modelFolderName= {modelFolder} and isTestFolder={isTestModel}')
        # PRELIMINARY STEPS for getting the input folder and creating respective output folder

        # 1) Getting INPUT FILES

        inputDIR = os.path.join(
            rootModelsDirName, modelFolder, "test" if isTestModel else "train")
        print(f'Working on {modelFolder} in folder {inputDIR}')
        # print(os.path.isdir(inputDIR))

        # Getting the list of all mesh in the directory 'modelFolder'
        inputModels = []
        INPUT_EXTENTION = ".ply"
        # Iterate directory
        for path in os.listdir(inputDIR):
            # check if current path is an expected file
            if os.path.isfile(os.path.join(inputDIR, path)) and os.path.join(inputDIR, path).endswith(INPUT_EXTENTION):
                # append only the file name
                inputModels.append(os.path.splitext(path)[0])
        # print(inputModels)

        # 3) Voxelizing all input files
        for path in inputModels:
            filename = Helper.getFullPathForModel(
                path, isTestModel, outputFolderName, isMesh=False, hasRotaions=True)
            #print(path)  # ,filename
            doThis(Helper.importVoxelGrid(filename).get_voxels(), VOXEL_GRID_SIZE)

forEach(Helper.describeVoxels)