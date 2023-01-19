import numpy as np
from HelperClass import HelperClass as Helper

# DEMO CALLS
model = "monitor_0031"
isTestModel = False

def getVGRotateOnZ(voxelGrid, degree):
    voxels = voxelGrid.get_voxels()
    array = []
    for i in range(len(voxels)): 
        x,y,z = voxels[i].grid_index
        newrow = [x, y, z]
        array.append(newrow)
    
    A = np.array(array)

    #grid_index_array = np.array(list(map(lambda x:x.grid_index,voxels)))
    
    # getting rotation matrix see Rz() https://en.wikipedia.org/wiki/Rotation_matrix
    R = np.eye(3) # ID matrix
    rz = degree

    R[2, 2] = 1
    R[0, 0] = np.cos(rz)
    R[0, 1] = -np.sin(rz)
    R[1, 0] = np.sin(rz)
    R[1, 1] = np.cos(rz)

    ROTATED = R.dot(A.T).T

    return Helper.getVoxelGridFromArray(ROTATED)

def getVGRotateOnY(voxelGrid, ry):
    grid_index_array = np.array(list(map(lambda x:x.grid_index,voxelGrid.get_voxels())))
    
    # getting rotation matrix see Ry() https://en.wikipedia.org/wiki/Rotation_matrix
    R = np.eye(3) # ID matrix
    R[1, 1] = 1

    R[0, 0] = np.cos(ry)
    R[0, 2] = np.sin(ry)
    R[2, 0] = -np.sin(ry)
    R[2, 2] = np.cos(ry)

    return Helper.getVoxelGridFromArray(R.dot(grid_index_array.T).T)

def getVGRotateOnX(voxelGrid, rx):
    grid_index_array = np.array(list(map(lambda x:x.grid_index,voxelGrid.get_voxels())))
    
    # getting rotation matrix see Rx() https://en.wikipedia.org/wiki/Rotation_matrix
    R = np.eye(3) # ID matrix
    R[0, 0] = 1
    R[1, 1] = np.cos(rx)
    R[1, 2] = -np.sin(rx)
    R[2, 1] = np.sin(rx)
    R[2, 2] = np.cos(rx)

    return Helper.getVoxelGridFromArray(R.dot(grid_index_array.T).T)

def getVGRotated(voxelGrid, rx=0,ry=0,rz=0):
    grid_index_array = np.array(list(map(lambda x:x.grid_index,voxelGrid.get_voxels())))
    
    # getting rotation matrix see https://en.wikipedia.org/wiki/Rotation_matrix
    R = np.eye(3) # ID matrix
    
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
Helper.show(getVGRotateOnZ(voxelGrid,np.pi/2))