from HelperClass import HelperClass as Helper

# DEMO CALLS
VOXEL_GRID_SIZE = 32
PADDING = 0 # PADDING is added twice to the right

outputDirName = "Test"
isTestModel = False
model = "sofa_0001" #"table_0116" #ok with /64 and "table_0361" ok only with export with pcd

current_inputModel, current_outputModel = Helper.getFoldersFromModel(model,isTestModel, outputDirName)
print(current_inputModel,current_outputModel)

# checking if the input file is present
#print("IS FILE PRESENT:",os.path.isfile(current_inputModel))

# importing the mesh
mesh = Helper.importMesh(current_inputModel)#.compute_vertex_normals()

# No need for scaling here, everting is done in voxelization
#mesh.scale(max(mesh.get_max_bound() - mesh.get_min_bound())/SIZE, mesh.get_center())

# getting the voxel size required OVERPASSES
# voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / Helper.VOXEL_SIZE_DIVIDER
# print(f'maxBound={mesh.get_max_bound()}, minBound={mesh.get_min_bound()}, center={mesh.get_center()}')
# print(f'voxel_size = {voxel_size:e}')
# print(f'Input mesh has {len(mesh.vertices)} vertices and {len(mesh.triangles)} triangles')

# mesh_smp = mesh.simplify_vertex_clustering(voxel_size=voxel_size,contraction=o3d.geometry.SimplificationContraction.Average)
# print(f'Simplified mesh has {len(mesh_smp.vertices)} vertices and {len(mesh_smp.triangles)} triangles')

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
