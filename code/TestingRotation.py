import numpy as np
from HelperClass import HelperClass as Helper

# DEMO CALLS
model = "monitor_0031"
isTestModel = False

def getVGRotated(voxelGrid, rx=0,ry=0,rz=0):
    grid_index_array = np.array(list(map(lambda x:x.grid_index,voxelGrid.get_voxels())))
    
    # getting rotation matrix see https://en.wikipedia.org/wiki/Rotation_matrix
    R = np.eye(3) # ID matrix, can also use np.zeros((3,3))
    
    a = rz
    b = ry
    g = rx
    R[0, 0] = np.cos(a)*np.cos(b)
    R[0, 1] = np.cos(a)*np.sin(b)*np.sin(g)-np.sin(a)*np.cos(g)
    R[0, 2] = np.cos(a)*np.sin(b)*np.cos(g)+np.sin(a)*np.sin(g)
    R[1, 0] = np.sin(a)*np.cos(b)
    R[1, 1] = np.sin(a)*np.sin(b)*np.sin(g)+np.cos(a)*np.cos(g)
    R[1, 2] = np.sin(a)*np.sin(b)*np.cos(g)-np.cos(a)*np.sin(g)
    R[2, 0] = -np.sin(b)
    R[2, 1] = np.cos(b)*np.sin(g)
    R[2, 2] = np.cos(b)*np.cos(g)
    
    return Helper.getVoxelGridFromArray(R.dot(grid_index_array.T).T)

current_inputModel,current_outputModel = Helper.getFoldersFromModel(model,isTestModel,"Output_v3")
voxelGrid = Helper.importVoxelGrid(current_outputModel)
Helper.show(voxelGrid)

Helper.show(getVGRotated(voxelGrid,rz=np.pi/2))