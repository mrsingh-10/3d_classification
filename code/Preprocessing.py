import numpy as np
from HelperClass import HelperClass as Helper

# def normalize(data):
#     mean = np.mean(data, axis=0)
#     std = np.std(data, axis=0)
#     return (data - mean) / std

# # Example usage:
# data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# normalized_data = normalize(data)
# print("before:",data)
# print("after:",normalized_data)

import numpy as np
import open3d as o3d

print(o3d.__version__)


def normalize_voxelgrid(voxelgrid):
    voxelgrid_np = np.array(list(map(lambda x:x.grid_index,voxelgrid.get_voxels())))
    mean = np.mean(voxelgrid_np, axis=0)
    std = np.std(voxelgrid_np, axis=0)
    normalized_voxelgrid_np = (voxelgrid_np - mean) / std
    return normalized_voxelgrid_np


# Example usage:
model = "chair_0986"
isTestModel = True
importFileName = Helper.getFullPathForModel(
    model, isTestModel, "Output_v3", isMesh=False)
voxelgrid = Helper.importVoxelGrid(importFileName)
#Helper.show(voxelgrid)
normalized_voxelgrid_np = normalize_voxelgrid(voxelgrid)
print(type(normalized_voxelgrid_np))
normalized_voxelgrid_vg = Helper.getVoxelGridFromArray(normalized_voxelgrid_np)
Helper.showComposed([normalized_voxelgrid_vg])

pc=o3d.geometry.PointCloud()
pc.points=o3d.utility.Vector3dVector(normalized_voxelgrid_np)
#pc.scale(1 / np.max(pc.get_max_bound() - pc.get_min_bound()), center=pc.get_center())

voxelSize = 1/(32-(1))
Helper.show(Helper.getVoxelGridFromPointCloud(pc,1))


# end goal:
# import numpy as np
# from sklearn.preprocessing import StandardScaler

# def preprocess_voxelgrid(voxelgrid):
#     # Normalize the voxelgrid using the StandardScaler from scikit-learn
#     scaler = StandardScaler()
#     normalized_voxelgrid = scaler.fit_transform(voxelgrid.reshape(-1, 1))
#     normalized_voxelgrid = normalized_voxelgrid.reshape(voxelgrid.shape)

#     # Apply data augmentation techniques, such as rotation, scaling, and flipping
#     augmented_voxelgrids = []
#     for _ in range(num_augmentations):
#         augmented_voxelgrid = apply_augmentation(normalized_voxelgrid)
#         augmented_voxelgrids.append(augmented_voxelgrid)

#     return augmented_voxelgrids

# def apply_augmentation(voxelgrid):
#     # Example augmentation: random rotation
#     random_rotation = generate_random_rotation()
#     rotated_voxelgrid = apply_rotation(voxelgrid, random_rotation)

#     # Add additional augmentations as needed
#     ...

#     return rotated_voxelgrid

# # Example usage:
# voxelgrid = load_voxelgrid_from_file(filepath)
# preprocessed_voxelgrids = preprocess_voxelgrid(voxelgrid)
