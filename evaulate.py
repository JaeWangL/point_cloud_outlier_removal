import open3d as o3d

from src.dataLoader.point_cloud_loader import DataLoader
from src.optimizer.point_cloud_optimizer import PointCloudOptimizer
from src.processor.noiseFilter.radius_outlier_removal import RadiusOutlierRemoval
from src.processor.noiseFilter.statistical_outlier_removal import StatisticalOutlierRemoval


def evaluation_func_example(original_cloud: o3d.geometry.PointCloud, processed_cloud: o3d.geometry.PointCloud) -> float:
    original_count = len(original_cloud.points)
    processed_count = len(processed_cloud.points)

    if original_count == 0:
        return float('inf')

    reduction_percentage = 100 * (original_count - processed_count) / original_count
    # Lower scores indicate less aggressive filtering
    return reduction_percentage


filename = 'CSite1_orig-utm.pcd'
data_loader = DataLoader(filename)
point_cloud = data_loader.load_data()

# Step1. Noise Filter
noise_optimizer = PointCloudOptimizer(point_cloud, evaluation_func_example, filename, 'noise_filter.txt')
noise_optimizer.add_processing_options(StatisticalOutlierRemoval, {
    'nb_neighbors': [10, 20, 30],
    'std_ratio': [1.0, 2.0, 3.0]
})
noise_optimizer.add_processing_options(RadiusOutlierRemoval, {
    'nb_points': [5, 10, 15],
    'radius': [0.05, 0.1, 0.15]
})
best_filter, best_score = noise_optimizer.process()
