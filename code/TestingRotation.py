import numpy as np
from HelperClass import HelperClass as Helper

# DEMO CALLS
model = "monitor_0031"
isTestModel = False

current_inputModel,current_outputModel = Helper.getFoldersFromModel(model,isTestModel,"Output_v3")
voxelGrid = Helper.importVoxelGrid(current_outputModel)
Helper.show(voxelGrid)

Helper.show(Helper.getVGRotated(voxelGrid,rz=np.pi/2))