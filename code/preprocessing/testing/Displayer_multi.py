import sys
import os
from pathlib import Path

# TO ADD preprocessing as module
path = Path(__file__)
while (path.stem != "code"):
    path = path.parent
sys.path.append(os.fspath(path.absolute()))

from preprocessing.HelperClass import HelperClass as Helper

import copy
import numpy as np

# PROBLEMS:
# NOT PRESENT: "table_0361"
# REMOVED UPPER PART of table_0116

# DEMO CALLS


def importMesh(path):
    # Importing mesh
    mesh = Helper.importMesh(path)
    # Scaling
    mesh.scale(max(mesh.get_max_bound() - mesh.get_min_bound()) /
               32, mesh.get_center())
    # mesh.compute_vertex_normals()
    return mesh

def process(mesh, i):
    m = copy.deepcopy(mesh)
    R = m.get_rotation_matrix_from_xyz((0, 0, 5*np.pi / 8))
    m.rotate(R, center=(0, 0, 0))
    m.translate((i*32, 0, 0))
    m.paint_uniform_color([1, 0.781, 0.254])
    return m


l = ["chair_0900", "chair_0902", "chair_0944", "chair_0952", "chair_0954",
     "chair_0980", "chair_0983", "chair_0986", "chair_0987", "chair_0989"]
#  "monitor_0471", "monitor_0469", "monitor_0470"]
l = ["monitor_0470", "monitor_0471", "monitor_0502", "monitor_0472",
     "monitor_0469", "monitor_0508", "monitor_0506", "monitor_0522", "monitor_0512",
     "monitor_0510"]
#l = [ "dresser_0"+str(i) for i in range(205,207)]


l = ["chair_0900", "chair_0902", "chair_0944", "chair_0952", "chair_0954",
     "chair_0980", "chair_0983", "chair_0986", "chair_0987", "chair_0989"]

m = []
v = []
# Importing mesh
i = 9
for i, path in enumerate(l[i:i+1]):
    isTestModel = True
    filename = Helper.getFullPathForModel(
        path, isTestModel, "ModelNet10", isMesh=True, hasRotaions=False)
    mesh = importMesh(filename)
    m.append(process(mesh, i))
    v.append(Helper.getVoxelGridFromMesh(mesh))
    print(i, path)

# Showing mesh with BBs
Helper.showComposed(v)

