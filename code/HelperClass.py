import os
import numpy as np
import open3d as o3d

# TODO: Bring folder creation inside the helper

class HelperClass:
    VOXEL_GRID_SIZE = 32
    SAMPLES = VOXEL_GRID_SIZE**3         # Samples to be sampled from meshes
    VOXEL_SIZE = 1/(VOXEL_GRID_SIZE - 1)        # L/W/H of each voxel --> 1/(voxelGridSize-(1+padding*2)) 0 Padding
    INPUT_EXTENTION = ".off"
    OUTPUT_EXTENTION = ".ply"
    VOXEL_GRID_FOLDER = "Output"

    # TODO remove all classmethods or the constructor
    def __init__(self,VOXEL_GRID_SIZE=32,INPUT_EXTENTION=".off",OUTPUT_EXTENTION = ".ply"):
        self.VOXEL_GRID_SIZE = VOXEL_GRID_SIZE
        self.SAMPLES = VOXEL_GRID_SIZE**3
        self.VOXEL_SIZE = 1/VOXEL_GRID_SIZE
        self.INPUT_EXTENTION = INPUT_EXTENTION
        self.OUTPUT_EXTENTION = OUTPUT_EXTENTION
    
    # TRANSFORMATION METHODS
    # POINT CLOUD
    @classmethod
    def getPointCloudFromMesh(cls,mesh, N=SAMPLES, poisson=False):
        if(poisson):
            return mesh.sample_points_poisson_disk(N)
        return mesh.sample_points_uniformly(number_of_points=N)
    
    @classmethod
    def getVoxelGridFromArray(cls,ThreeDimArray):
        pc=o3d.geometry.PointCloud()
        pc.points=o3d.utility.Vector3dVector(ThreeDimArray)
        return cls.getVoxelGridFromPointCloud(pc,voxelSize=1)

    # VOXEL GRID
    @classmethod
    def getVoxelGridFromPointCloud(cls,pcd, voxelSize=VOXEL_SIZE):
        return o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,voxel_size=voxelSize)

    @classmethod
    def getVoxelGridFromMesh(cls,mesh, voxelGridSize=VOXEL_GRID_SIZE, padding=0):
        voxelSize = 1/(voxelGridSize-(1+padding*2))
        
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
    def getFoldersFromModel(cls,model, isTestModel, outputDirName):
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

    @classmethod
    def describeVoxels(cls,voxels,voxelGridSize, displayMin=True, displayMax=True,):
        displayTotal=True
        maxArray = np.array([0, 0, 0],np.int32)
        minArray = np.array([voxelGridSize, voxelGridSize,voxelGridSize],np.int32)

        array = np.zeros((voxelGridSize,voxelGridSize,voxelGridSize,1))
        for i in range(len(voxels)): 
            x,y,z = voxels[i].grid_index
            array[x][y][z] = 1
            maxArray = np.maximum(maxArray, voxels[i].grid_index)
            minArray = np.minimum(minArray, voxels[i].grid_index)

        # to check
        tot = 0
        for x,y,z in ((a,b,c) for a in range (voxelGridSize) for b in range (voxelGridSize) for c in range (voxelGridSize)):
            value = array[x][y][z]
            if value > 0:
                #print(x,y,z,value)
                tot += 1
        
        string = f'totalVoxels={tot}' if displayTotal else ""
        string += f', maxArray={maxArray}' if displayMax else ""
        string += f', minArray={minArray}' if displayMin else ""
        final_str = f'{string}'

        print(final_str)
    
    @classmethod
    def createOutputFoldersForModelFolder(cls,modelFolder,outputDirName):
        baseDIR = os.path.dirname(__file__)
        outputDIR = os.path.join(baseDIR,outputDirName)
        modelFolderOutput = os.path.join(outputDIR,modelFolder)

        #print(f"Creating folder {outputDIR}")
        if not os.path.exists(outputDIR):os.makedirs(outputDIR)
        #print(f"Creating folder {modelFolderOutput}")
        if not os.path.exists(modelFolderOutput):os.makedirs(modelFolderOutput)
        #print(f'Creating folder {os.path.join(modelFolderOutput,"test")}')
        if not os.path.exists(os.path.join(modelFolderOutput,"test")):os.makedirs(os.path.join(modelFolderOutput,"test"))
        #print(f'Creating folder {os.path.join(modelFolderOutput,"train")}')
        if not os.path.exists(os.path.join(modelFolderOutput,"train")): os.makedirs(os.path.join(modelFolderOutput,"train"))

    @classmethod
    def createOutputFoldersForModel(cls,model,outputDirName):
        temp = model.split("_")
        temp.pop()
        modelFolder = "_".join(map(str,temp))
        cls.createOutputFoldersForModelFolder(modelFolder,outputDirName)
    