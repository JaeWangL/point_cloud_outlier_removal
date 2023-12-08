import open3d as o3d

from src.processor.base_processor import BasePointCloudProcessor


class RadiusOutlierRemoval(BasePointCloudProcessor):
    def apply(self, point_cloud: o3d.geometry.PointCloud, nb_points: int = 16, radius: float = 0.05) -> o3d.geometry.PointCloud:
        """
        Removes radius-based outliers from a point cloud using Open3D's remove_radius_outlier method.
        :param point_cloud: The input Open3D PointCloud object.
        :param nb_points: Number of points within the specified radius.
        :param radius: The radius to search for neighboring points.
        :return: The filtered Open3D PointCloud object.
        """
        filtered_cloud, _ = point_cloud.remove_radius_outlier(nb_points, radius)
        return filtered_cloud
