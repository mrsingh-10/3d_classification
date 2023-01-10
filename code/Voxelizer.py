import os
import open3d as o3d
import time
from joblib import Parallel, delayed
from HelperClass import HelperClass as Helper


SAMPLES = 64**3         # Samples to be sampled from meshes
VOXEL_SIZE = 0.01        # L/W/H of each voxel
INPUT_EXTENTION = ".off"
OUTPUT_EXTENTION = ".ply"

def meshToVoxel(model,test):
    # IMPORT STEP
    print("Current model:", model)
    current_inputModel,current_outputModel = Helper.getFoldersFromModel(model,isTestModel=test)
    
    # Importing the mesh from the disk
    mesh = Helper.importMesh(current_inputModel) #.compute_vertex_normals()

    # VOXELIZATION STEP
    # Clustering to reduce the number and aggregate voxels
    voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / 32
    #print(f'voxel_size = {voxel_size:e}')
    #print(f'Input mesh has {len(mesh.vertices)} vertices and {len(mesh.triangles)} triangles')

    mesh_smp = mesh.simplify_vertex_clustering(voxel_size=voxel_size,contraction=o3d.geometry.SimplificationContraction.Average)
    #print(f'Simplified mesh has {len(mesh_smp.vertices)} vertices and {len(mesh_smp.triangles)} triangles')

    # Voxelization
    voxelGrid = Helper.getVoxelGridFromMesh(mesh_smp,0.01)

    # EXPORT STEP
    # Exporting the Simplified vertex clusted version of the mesh
    Helper.exportVoxelGrid(current_outputModel,voxelGrid)

# DEMO CALLS
baseDIR = os.path.dirname(__file__)
modelNetDIR = os.path.join(baseDIR,"ModelNet10")

# test = True
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
        if os.path.isfile(os.path.join(inputDIR, path)) and os.path.join(inputDIR, path).endswith(INPUT_EXTENTION):
            # append only the file name
            inputModels.append(os.path.splitext(path)[0])
    #print(inputModels)

    # 2) Creating Output Directories
    outputDIR = os.path.join(baseDIR,"Output")
    modelFolderOutput = os.path.join(outputDIR,modelFolder)

    if not os.path.exists(outputDIR):os.makedirs(outputDIR)
    if not os.path.exists(modelFolderOutput):os.makedirs(modelFolderOutput)
    if not os.path.exists(os.path.join(modelFolderOutput,"test")):os.makedirs(os.path.join(modelFolderOutput,"test"))
    if not os.path.exists(os.path.join(modelFolderOutput,"train")): os.makedirs(os.path.join(modelFolderOutput,"train"))

    # 3) Voxelizing all input files
    t = time.time()
    Parallel(n_jobs=4)(delayed(meshToVoxel)(path,test) for path in inputModels) #n_jobs=-2 # use all cpu exept 1
    print("Time:",time.time() - t)