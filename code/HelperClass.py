import os
import numpy as np
import open3d as o3d

# TODO: Bring folder creation inside the helper

class HelperClass:
    SAMPLES = 64**3         # Samples to be sampled from meshes
    VOXEL_SIZE = 0.01        # L/W/H of each voxel
    INPUT_EXTENTION = ".off"
    OUTPUT_EXTENTION = ".ply"
    VOXEL_SIZE_DIVIDER = 64
    VOXEL_GRID_FOLDER = "Output"


    def __init__(self,SAMPLES=64**3,VOXEL_SIZE=0.01,INPUT_EXTENTION=".off",OUTPUT_EXTENTION = ".ply",VOXEL_SIZE_DIVIDER=64):
        self.SAMPLES = SAMPLES
        self.VOXEL_SIZE = VOXEL_SIZE
        self.INPUT_EXTENTION = INPUT_EXTENTION
        self.OUTPUT_EXTENTION = OUTPUT_EXTENTION
        self.VOXEL_SIZE_DIVIDER = VOXEL_SIZE_DIVIDER
    
    # TRANSFORMATION METHODS
    # POINT CLOUD
    @classmethod
    def getPointCloudFromMesh(cls,mesh, N=SAMPLES, poisson=False):
        if(poisson):
            return mesh.sample_points_poisson_disk(N)
        return mesh.sample_points_uniformly(number_of_points=N)

    # VOXEL GRID
    @classmethod
    def getVoxelGridFromPointCloud(cls,pcd, voxelSize=VOXEL_SIZE):
        return o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,voxel_size=voxelSize)

    @classmethod
    def getVoxelGridFromMesh(cls,mesh, voxelSize=VOXEL_SIZE):
        ## Fit to unit cube.
        mesh.scale(1 / np.max(mesh.get_max_bound() - mesh.get_min_bound()), center=mesh.get_center())
        return o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh, voxel_size=voxelSize)

    # EXPORT METHODS
    @classmethod
    def exportPointCloud(cls,filename,pointCloud,compressed=False):
        o3d.io.write_point_cloud(filename, pointCloud, write_ascii=True, compressed=compressed, print_progress=True)

    @classmethod
    def exportVoxelGrid(cls,filename,voxelGrid,compressed=False):
        o3d.io.write_voxel_grid(filename, voxelGrid, write_ascii=False, compressed=compressed, print_progress=False)
        
    # IMPORT METHODS
    # MESH from os path
    @classmethod
    def importMesh(cls,filename):
        return o3d.io.read_triangle_mesh(filename)

    @classmethod
    def importPointCloud(cls,filename):
        return o3d.io.read_point_cloud(filename, format='auto',remove_nan_points=False, remove_infinite_points=False, print_progress=True)

    @classmethod
    def importVoxelGrid(cls,filename):
        return o3d.io.read_voxel_grid(filename, format='auto', print_progress=True)

    # UTILs
    @classmethod
    def show(cls,view,standalone=False):
        cls.showComposed([view],standalone)

    @classmethod
    def showComposed(cls,view,standalone=False):
        if(standalone):
            o3d.visualization.draw(view)
        else:
            o3d.visualization.draw_geometries(view)
    @classmethod
    def getFoldersFromModel(cls,model, isTestModel, outputDirName=VOXEL_GRID_FOLDER):
        baseDIR = os.path.dirname(__file__)
        test = isTestModel

        temp = model.split("_")
        temp.pop()
        modelFolder = "_".join(map(str,temp))

        modelNetDIR = os.path.join(baseDIR,"ModelNet10")
        outputDIR = os.path.join(baseDIR,outputDirName)
        modelFolderOutput = os.path.join(outputDIR,modelFolder)

        current_inputModel = os.path.join(modelNetDIR,modelFolder,"test" if test else "train",model+cls.INPUT_EXTENTION)
        current_outputModel = os.path.join(modelFolderOutput,"test" if test else "train",model+cls.OUTPUT_EXTENTION)
        return (current_inputModel,current_outputModel)
