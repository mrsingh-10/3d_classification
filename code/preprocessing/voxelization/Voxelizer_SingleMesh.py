import sys
import os
from pathlib import Path

# TO ADD preprocessing as module
path = Path(__file__)
while (path.stem != "code"):
    path = path.parent
sys.path.append(os.fspath(path.absolute()))

from preprocessing.HelperClass import HelperClass as Helper

# DEMO CALLS
VOXEL_GRID_SIZE = 32
PADDING = 0 # PADDING is added twice to the right

outputDirName = "Test"
isTestModel = False
model = "sofa_0001"

current_inputModel, current_outputModel = Helper.getFoldersFromModel(model,isTestModel, outputDirName)
print(current_inputModel,current_outputModel)

# importing the mesh
mesh = Helper.importMesh(current_inputModel)#.compute_vertex_normals()

# GET & SHOW POINT CLOUD
pcd = Helper.getPointCloudFromMesh(mesh)
Helper.show(pcd)

# EXPORT VOXELGRID OF THE Simplified vertex clustering
voxelGrid = Helper.getVoxelGridFromMesh(mesh,VOXEL_GRID_SIZE,PADDING)
Helper.describeVoxels(voxelGrid.get_voxels(),VOXEL_GRID_SIZE)

Helper.show(voxelGrid)

# EXPORTING
Helper.createOutputFoldersForModel(model,outputDirName)
Helper.exportVoxelGrid(current_outputModel,voxelGrid)

## Import voxelgrid
Helper.show(Helper.importVoxelGrid(current_outputModel))
