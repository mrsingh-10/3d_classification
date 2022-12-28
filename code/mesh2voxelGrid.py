import trimesh
import os
from trimesh.viewer import windowed

# UTIL
def showScene(*scenes):
    scene = trimesh.Scene([scenes])
    windowed.SceneViewer(scene, resolution=(400,400))

# POINT CLOUD
def getPointCloud(mesh,num_points=2048):
    return trimesh.PointCloud(mesh.sample(num_points))

# VOXEL GRID
def getVoxelGrid(mesh, patch=0.5):
    return mesh.voxelized(patch).hollow()

# TODO: NOT WORKING PROPERLY
def exportVoxelGrid(voxelGrid,name):
    print(voxelGrid.scale)
    voxelGrid.export(file_obj=name,file_type="binvox")
    #voxelGrid.export(file_obj=name,file_type="binvox")

# DEMO CALLS
baseDIR = os.path.dirname(os.path.abspath("ModelNet10"))

modelNetFolder = os.path.abspath("ModelNet10")
monitor = os.path.join(modelNetFolder,"monitor/test/monitor_0466.off")
print("IS FILE PRESENT:",os.path.isfile(monitor))

# LOAD A MESH
mesh = trimesh.load(monitor)
vertices = trimesh.points.PointCloud(mesh.vertices)

showScene(mesh,vertices)

# GET AND SHOW POINT CLOUD
showScene(getPointCloud(mesh,4096))

# GET AND SHOW VOXEL GRID --> TODO:SAVE
voxelGrid = getVoxelGrid(mesh,0.5)#.apply_scale(2)
showScene(voxelGrid.as_boxes())
exportVoxelGrid(voxelGrid,monitor+"_out.binvox")