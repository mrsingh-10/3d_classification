from HelperClass import HelperClass as Helper

# PROBLEMS:
# NOT PRESENT: "table_0361"
# REMOVED UPPER PART of table_0116

# DEMO CALLS
model = "table_0361"
isTestModel = False
current_inputModel,current_outputModel = Helper.getFoldersFromModel(model,isTestModel)

mesh = Helper.importMesh(current_inputModel)
#Helper.show(mesh)

# getting bounding box 
import open3d as o3d

bb = mesh.get_axis_aligned_bounding_box()
bb.color = (255,0,0)
print(bb)
o3d.visualization.draw_geometries([mesh,bb])

print(bb.get_max_bound() - bb.get_min_bound())
print(max(mesh.get_max_bound() - mesh.get_min_bound())/32)

mesh.scale(max(mesh.get_max_bound() - mesh.get_min_bound())/32, mesh.get_center())

bb2 = mesh.get_axis_aligned_bounding_box()
bb2.color = (0,0,255)
print(bb2)
o3d.visualization.draw_geometries([mesh,bb,bb2])

#mesh_smp = mesh.simplify_vertex_clustering(voxel_size=0.01,contraction=o3d.geometry.SimplificationContraction.Average)
#Helper.showComposed([mesh_smp,bb,bb2])
#print(f'Simplified mesh has {len(mesh_smp.vertices)} vertices and {len(mesh_smp.triangles)} triangles')
# Voxelization
voxelGrid = Helper.getVoxelGridFromMesh(mesh,0.1/3)

o3d.visualization.draw_geometries([voxelGrid])








# POINT CLOUD
#pcd = Helper.getPointCloudFromMesh(mesh,N=64**3)
#Helper.show(pcd)

# VoxelGrid -> for chair_0876 I need to use 3*100
#           -> for desk_0040 I need to use 10
#           -> for desk_0153 I need to use 1
#voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / Helper.VOXEL_SIZE_DIVIDER
#voxel = Helper.getVoxelGridFromPointCloud(pcd,voxel_size)
#Helper.show(voxel,False)

# Exported VoxelGrid
#Helper.show(Helper.getVoxelGridFromMesh(mesh))
