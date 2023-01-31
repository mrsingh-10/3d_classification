import open3d as o3d
from HelperClass import HelperClass as Helper
import os
from random import sample

print(o3d.__version__)
# Open a file
# DEMO CALLS

VOXEL_GRID_SIZE = 32
outputFolderName = "Output_ROTATED_v4"


def getKPartitionsGathered(folderName, K=5):
    # dooing for all the models
    baseDIR = os.path.dirname(__file__)
    rootModelsDirName = os.path.join(baseDIR, folderName)

    models = ["bathtub", "bed", "chair", "desk", "dresser",
              "monitor", "night_stand", "sofa", "table", "toilet"]
    # models = ["desk"]

    # PUSHING ALL models in allModels
    allModels = {}
    for modelFolder, isTestModel in ((x, y) for x in models for y in (True, False)):
        #print(f'current modelFolderName= {modelFolder} and isTestFolder={isTestModel}')
        # PRELIMINARY STEPS for getting the input folder and creating respective output folder

        # 1) Getting INPUT FILES
        inputDIR = os.path.join(
            rootModelsDirName, modelFolder, "test" if isTestModel else "train")
        #print(f'Working on {modelFolder} in folder {inputDIR}')
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
        # print(2, inputModels)
        allModels[modelFolder+"/" +
                  ("test" if isTestModel else "train")+"/"] = inputModels

    # DIVIDING allModels into K Partitions
    k_sets_indexes = [i for i in range(0, K)]
    randomsGlobal = [0 for _ in range(0, K)]

    k_sets = [[] for _ in range(0, K)]

    # print(f"k_sets_indexes: {k_sets_indexes}, K={K}")
    # print(f"Randoms: {randomsGlobal}")
    # print(f"k_sets: {k_sets}")
    for key in allModels:
        # print(key, len(allModels[key]))
        for v in allModels[key]:
            index = sample(k_sets_indexes, 1)
            k_sets[index[0]].append(key+""+v)
            # print(index)
            randomsGlobal[index[0]] += 1

    # print(f"k_sets: {k_sets}", sep='\n')
    # print(k_sets,sep='\n')
    print(f"Randoms: {randomsGlobal}")
    return k_sets

def getKPartitionsFolderized(folderName, K, folderTest):
    # dooing for all the models
    baseDIR = os.path.dirname(__file__)
    rootModelsDirName = os.path.join(baseDIR, folderName)

    models = ["bathtub", "bed", "chair", "desk", "dresser",
              "monitor", "night_stand", "sofa", "table", "toilet"]
    # models = ["desk"]

    # PUSHING ALL models in allModels
    allModels = {}

    for modelFolder in models:
        # print(f'current modelFolderName= {modelFolder} and isTestFolder={isTestModel}')
        # PRELIMINARY STEPS for getting the input folder and creating respective output folder

        # 1) Getting INPUT FILES
        inputDIR = os.path.join(
            rootModelsDirName, modelFolder, "test" if folderTest else "train")
        # print(f'Working on {modelFolder} in folder {inputDIR}')
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
        # print(2, inputModels)
        allModels[modelFolder] = inputModels

    # DIVIDING allModels into K Partitions
    k_sets_indexes = [i for i in range(0, K)]
    randomsGlobal = [0 for _ in range(0, K)]

    # array di K dictionaries inizializzati a empty
    k_sets = [{} for _ in range(0, K)]
    for key in allModels:
        print(key, len(allModels[key]))
        for v in allModels[key]:
            # of the bucket
            index = sample(k_sets_indexes, 1)[0]
            if not k_sets[index].keys().__contains__(key):
                k_sets[index][key] = []
            k_sets[index][key].append(v)
            # print(index)
            randomsGlobal[index] += 1

    print(f"Randoms: {randomsGlobal}")
    return k_sets

sets = getKPartitionsGathered(outputFolderName, 5)

for set in sets:
    for elem in set[:10]:
        print(elem)
    print("------\n")

print([len(s) for s in sets])

sets = getKPartitionsFolderized(outputFolderName, 5, False)

for idx, set in enumerate(sets):
    print(idx, len(set["bed"]))


print(len(sets[0]["bed"]))