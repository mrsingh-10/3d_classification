from HelperClass import HelperClass as Helper

import os
import open3d as o3d

# DEMO CALLS

outputDirName = "Test"
isTestModel = True
model = "bathtub_0107" #"table_0116" #ok with /64
                       # "table_0361" ok only with export with pcd

current_inputModel, current_outputModel = Helper.getFoldersFromModel(model,isTestModel, outputDirName)
print(current_inputModel,current_outputModel)

print("IS FILE PRESENT:",os.path.isfile(current_inputModel))

def createFoldersForModel(model):
    temp = model.split("_")
    temp.pop()
    modelFolder = "_".join(map(str,temp))
    
    baseDIR = os.path.dirname(__file__)
    outputDIR = os.path.join(baseDIR,outputDirName)
    modelFolderOutput = os.path.join(outputDIR,modelFolder)

    if not os.path.exists(outputDIR):os.makedirs(outputDIR)
    if not os.path.exists(modelFolderOutput):os.makedirs(modelFolderOutput)
    if not os.path.exists(os.path.join(modelFolderOutput,"test")):os.makedirs(os.path.join(modelFolderOutput,"test"))
    if not os.path.exists(os.path.join(modelFolderOutput,"train")): os.makedirs(os.path.join(modelFolderOutput,"train"))

mesh = Helper.importMesh(current_inputModel)#.compute_vertex_normals()
mesh.scale(max(mesh.get_max_bound() - mesh.get_min_bound())/32, mesh.get_center())

# getting the voxel size required
voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / Helper.VOXEL_SIZE_DIVIDER
print(f'maxBound={mesh.get_max_bound()}, minBound={mesh.get_min_bound()}, center={mesh.get_center()}')
print(f'voxel_size = {voxel_size:e}')
print(f'Input mesh has {len(mesh.vertices)} vertices and {len(mesh.triangles)} triangles')

mesh_smp = mesh.simplify_vertex_clustering(voxel_size=voxel_size,contraction=o3d.geometry.SimplificationContraction.Average)
print(f'Simplified mesh has {len(mesh_smp.vertices)} vertices and {len(mesh_smp.triangles)} triangles')

# GET & SHOW POINT CLOUD
pcd = Helper.getPointCloudFromMesh(mesh_smp)
Helper.show(pcd)

# EXPORT VOXELGRID OF THE Simplified vertex clustering
voxelGrid = Helper.getVoxelGridFromMesh(mesh,0.1/3)
if(voxelGrid.has_voxels()):
    Helper.exportVoxelGrid(current_outputModel,voxelGrid)
else:
    print(voxelGrid)
    Helper.exportVoxelGrid(current_outputModel,Helper.getVoxelGridFromPointCloud(pcd,voxel_size))
    
#show(voxelGrid)

## Import voxelgrid
Helper.show(Helper.importVoxelGrid(current_outputModel))
