import open3d as o3d

from src.processor.base_processor import BasePointCloudProcessor


class StatisticalOutlierRemoval(BasePointCloudProcessor):
    def apply(self, point_cloud: o3d.geometry.PointCloud, nb_neighbors: int = 20, std_ratio: float = 2.0) -> o3d.geometry.PointCloud:
        """
        Removes statistical outliers from a point cloud using Open3D's remove_statistical_outlier method.
        :param point_cloud: The input Open3D PointCloud object.
        :param nb_neighbors: Number of neighbors to consider for each point.
        :param std_ratio: Standard deviation ratio.
        :return: The filtered Open3D PointCloud object.
        """
        filtered_cloud, _ = point_cloud.remove_statistical_outlier(nb_neighbors, std_ratio)
        return filtered_cloud
