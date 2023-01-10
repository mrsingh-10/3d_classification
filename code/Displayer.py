from HelperClass import HelperClass as Helper

# PROBLEMS:
# NOT PRESENT: "table_0361"
# REMOVED UPPER PART of table_0116

# DEMO CALLS
current_inputModel,current_outputModel = Helper.getFoldersFromModel(model = "bathtub_0107",isTestModel = True)

mesh = Helper.importMesh(current_inputModel)
Helper.show(mesh)
# POINT CLOUD
pcd = Helper.getPointCloudFromMesh(mesh,N=64**3)
Helper.show(pcd)

# VoxelGrid -> for chair_0876 I need to use 3*100
#           -> for desk_0040 I need to use 10
#           -> for desk_0153 I need to use 1
voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / Helper.VOXEL_SIZE_DIVIDER
voxel = Helper.getVoxelGridFromPointCloud(pcd,voxel_size)
Helper.show(voxel,False)

# Exported VoxelGrid
Helper.show(Helper.getVoxelGridFromMesh(mesh))
