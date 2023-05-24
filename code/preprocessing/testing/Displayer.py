import sys
import os
from pathlib import Path

# TO ADD preprocessing as module
path = Path(__file__)
while (path.stem != "code"):
    path = path.parent
sys.path.append(os.fspath(path.absolute()))

from preprocessing.HelperClass import HelperClass as Helper

# PROBLEMS:
# NOT PRESENT: "table_0361"
# REMOVED UPPER PART of table_0116

# DEMO CALLS
model = "chair_0957"
isTestModel = True
current_inputModel, current_outputModel = Helper.getFoldersFromModel(
    model, isTestModel, "Output_v3")


# Importing mesh
mesh = Helper.importMesh(current_inputModel)

# Getting bounding box
bb = mesh.get_axis_aligned_bounding_box()
bb.color = (255, 0, 0)
print(bb)

print(bb.get_max_bound() - bb.get_min_bound())
print(max(mesh.get_max_bound() - mesh.get_min_bound())/32)

# Scaling
mesh.scale(max(mesh.get_max_bound() - mesh.get_min_bound()) /
           32, mesh.get_center())

# Getting new BB
bb2 = mesh.get_axis_aligned_bounding_box()
bb2.color = (0, 0, 255)
print(bb2)

# Showing mesh with BBs
Helper.showComposed([mesh, bb, bb2])

# Voxelization
voxelGrid = Helper.getVoxelGridFromMesh(mesh, 32)

Helper.showComposed([voxelGrid])  # ,bb2

# POINT CLOUD
# pcd = Helper.getPointCloudFromMesh(mesh,N=64**3)
# Helper.show(pcd)

# VoxelGrid -> for chair_0876 I need to use 3*100
#           -> for desk_0040 I need to use 10
#           -> for desk_0153 I need to use 1
# voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / Helper.VOXEL_SIZE_DIVIDER
# voxel = Helper.getVoxelGridFromPointCloud(pcd,voxel_size)
# Helper.show(voxel,False)

# Exported VoxelGrid
# Helper.show(Helper.getVoxelGridFromMesh(mesh))

Helper.show(Helper.importVoxelGrid(current_outputModel))
