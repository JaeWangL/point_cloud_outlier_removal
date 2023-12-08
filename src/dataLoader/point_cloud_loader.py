import open3d as o3d
import os
import laspy
import numpy as np

from src.helpers.file_helpers import get_file_extension


class DataLoader:
    def __init__(self, filename: str) -> None:
        """
        Initializes the DataLoader with the specified file path.
        :param filename: The filename of point cloud file.
        """
        self.file_path = os.path.join("data", filename)

    def load_data(self) -> o3d.geometry.PointCloud:
        """
        Loads the point cloud data from the file with file_path.
        Data is generally loaded by o3d. But, If lidar file, we use _load_las_data
        :return: The loaded point cloud as an Open3D PointCloud object.
        """
        file_extension = get_file_extension(self.file_path)
        if file_extension == 'las' or file_extension == 'laz':
            return self._load_las_data()

        return o3d.io.read_point_cloud(self.file_path)

    def _load_las_data(self) -> o3d.geometry.PointCloud:
        """
        Loads a LAS file using laspy and converts it to an Open3D PointCloud.
        :return: The loaded point cloud as an Open3D PointCloud object.
        """
        las = laspy.read(self.file_path)
        points = np.vstack((las.x, las.y, las.z)).transpose()

        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)

        return point_cloud
