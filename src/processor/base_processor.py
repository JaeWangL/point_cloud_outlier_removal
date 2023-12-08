import open3d as o3d
from typing import Any


class BasePointCloudProcessor:
    def apply(self, point_cloud: o3d.geometry.PointCloud, **params: Any) -> o3d.geometry.PointCloud:
        """
        Apply a processing step to a point cloud. This method should be overridden by subclasses.
        :param point_cloud: The input point cloud.
        :param params: Parameters for the processing algorithm.
        :return: The processed point cloud.
        """
        pass
