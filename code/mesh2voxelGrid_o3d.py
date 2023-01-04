import os
import numpy as np
import open3d as o3d

SAMPLES = 64**3         # Samples to be sampled from meshes
VOXEL_SIZE = 0.01        # L/W/H of each voxel
INPUT_EXTENTION = ".off"
OUTPUT_EXTENTION = ".ply"

# models = ["bathtub", "bed", "chair", "desk", "dresser", "monitor", "night_stand", "sofa", "table", "toilet" ]

# UTILs
def show(view,standalone=False):
    if(standalone):
        o3d.visualization.draw([view])
    else:
        o3d.visualization.draw_geometries([view])

# MESH from os path
def getMesh(path):
    return o3d.io.read_triangle_mesh(path)

# POINT CLOUD
def getPointCloud(mesh, N=SAMPLES, poisson=False):
    if(poisson):
        return mesh.sample_points_poisson_disk(N)
    return mesh.sample_points_uniformly(number_of_points=N)

# VOXEL GRID
def getVoxelGridFromPointCloud(pcd, voxelSize=VOXEL_SIZE):
    return o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,voxel_size=voxelSize)

def getVoxelGridFromMesh(mesh, voxelSize=VOXEL_SIZE):
    ## Fit to unit cube.
    mesh.scale(1 / np.max(mesh.get_max_bound() - mesh.get_min_bound()), center=mesh.get_center())
    return o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh, voxel_size=voxelSize)

def exportPointCloud(filename,pointCloud,compressed=False):
    o3d.io.write_point_cloud(filename, pointCloud, write_ascii=True, compressed=compressed, print_progress=True)

def exportVoxelGrid(filename,voxelGrid,compressed=False):
    o3d.io.write_voxel_grid(filename, voxelGrid, write_ascii=False, compressed=compressed, print_progress=False)
    
def importPointCloud(filename):
    return o3d.io.read_point_cloud(filename, format='auto',remove_nan_points=False, remove_infinite_points=False, print_progress=True)

def importVoxelGrid(filename):
    return o3d.io.read_voxel_grid(filename, format='auto', print_progress=True)

# DEMO CALLS
baseDIR = os.path.dirname(__file__)

modelNetDIR = os.path.join(baseDIR,"ModelNet10")

test = False
model = "night_stand_0001" #.off
temp = model.split("_")
temp.pop()
modelFolder = "_".join(map(str,temp))

current_inputModel = os.path.join(modelNetDIR,modelFolder,"test" if test else "train",model+INPUT_EXTENTION)

outputDIR = os.path.join(baseDIR,"Output")
modelFolderOutput = os.path.join(outputDIR,modelFolder)

if not os.path.exists(outputDIR):os.makedirs(outputDIR)
if not os.path.exists(modelFolderOutput):os.makedirs(modelFolderOutput)
if not os.path.exists(os.path.join(modelFolderOutput,"test")):os.makedirs(os.path.join(modelFolderOutput,"test"))
if not os.path.exists(os.path.join(modelFolderOutput,"train")): os.makedirs(os.path.join(modelFolderOutput,"train"))

current_outputModel = os.path.join(modelFolderOutput,"test" if test else "train",model+OUTPUT_EXTENTION)
print(current_inputModel)
print(current_outputModel)
print("IS FILE PRESENT:",os.path.isfile(current_inputModel))

mesh = getMesh(current_inputModel) #.compute_vertex_normals()

voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / 32
print(f'voxel_size = {voxel_size:e}')
print(f'Input mesh has {len(mesh.vertices)} vertices and {len(mesh.triangles)} triangles')

mesh_smp = mesh.simplify_vertex_clustering(voxel_size=voxel_size,contraction=o3d.geometry.SimplificationContraction.Average)
print(f'Simplified mesh has {len(mesh_smp.vertices)} vertices and {len(mesh_smp.triangles)} triangles')

# GET & SHOW POINT CLOUD
show(getPointCloud(mesh_smp))

# EXPORT VOXELGRID OF THE Simplified vertex clustering
voxelGrid = getVoxelGridFromMesh(mesh_smp,0.01)
#show(voxelGrid)
exportVoxelGrid(current_outputModel,voxelGrid)

## Import voxelgrid
show(importVoxelGrid(current_outputModel))
