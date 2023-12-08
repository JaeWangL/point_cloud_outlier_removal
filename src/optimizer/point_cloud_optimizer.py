import os
from typing import Callable, Dict, List, Tuple, Type, Any
import itertools
import time
from tqdm import tqdm
import open3d as o3d

from src.helpers.file_helpers import get_filename_without_extension
from src.processor.base_processor import BasePointCloudProcessor


class PointCloudOptimizer:
    def __init__(self,
                 original_point_cloud: o3d.geometry.PointCloud,
                 evaluation_func: Callable[[o3d.geometry.PointCloud, o3d.geometry.PointCloud], float],
                 input_filename: str,
                 log_filename: str) -> None:
        """
        Initializes the optimizer with a point cloud, an evaluation function, and a log file.
        :param original_point_cloud: The original point cloud before processing.
        :param evaluation_func: A function that evaluates and returns a score
                                  based on the original and processed point clouds.
        :param input_filename: The name of the file for point cloud.
        :param log_filename: The name of the file for evaluation logs.
        """
        self.original_point_cloud = original_point_cloud
        self.evaluation_func = evaluation_func
        self.processing_options: List[Tuple[Type[BasePointCloudProcessor], Dict[str, List[Any]]]] = []

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        sub_folder_path = os.path.join("data", f"{get_filename_without_extension(input_filename)}_{timestamp}")
        os.makedirs(sub_folder_path, exist_ok=True)  # Create the subfolder
        self.logfile_path = os.path.join(sub_folder_path, log_filename)

    def add_processing_options(self,
                               processor_class: Type[BasePointCloudProcessor],
                               param_grid: Dict[str, List[Any]]) -> None:
        """
        Adds a processing class and its corresponding parameter grid to the optimizer.
        :param processor_class: The class of the processor to be used.
        :param param_grid: A dictionary where keys are parameter names and values are lists of possible values.
        """
        self.processing_options.append((processor_class, param_grid))

    def process(self) -> Tuple[Tuple[Type[BasePointCloudProcessor], Dict[str, Any]], float]:
        """
        Performs an exhaustive search over all added processor configurations to find the best one.
        :return: A tuple of the best processor configuration and its score.
        """
        best_score = float('inf')
        best_configuration = None

        # Below is for displaying with tqdm
        total_combinations = sum(len(list(itertools.product(*param_grid.values()))) for _, param_grid in self.processing_options)
        progress_bar = tqdm(total=total_combinations, desc='Evaluating Configurations')

        for processor_class, param_grid in self.processing_options:
            for param_combination in itertools.product(*param_grid.values()):
                param_dict = dict(zip(param_grid.keys(), param_combination))
                score = self._evaluate_processor(processor_class, param_dict)

                if score < best_score:
                    best_score = score
                    best_configuration = (processor_class, param_dict)

                progress_bar.update(1)

        progress_bar.close()
        return best_configuration, best_score

    def _evaluate_processor(self,
                            processor_class: Type[BasePointCloudProcessor],
                            param_dict: Dict[str, Any]) -> float:
        """
        Evaluates a single processor configuration and logs the result.
        :param processor_class: The class of the processor being evaluated.
        :param param_dict: Dictionary of parameters for the processor.
        :return: The score of the evaluated processor configuration.
        """
        start_time = time.time()
        processor_instance = processor_class()
        processed_point_cloud = processor_instance.apply(self.original_point_cloud, **param_dict)
        elapsed_time = time.time() - start_time
        score = self.evaluation_func(self.original_point_cloud, processed_point_cloud)

        self._log_results(processor_class.__name__, param_dict, elapsed_time, score)
        return score

    def _log_results(self,
                     processor_name: str,
                     params: Dict[str, Any],
                     time_taken: float,
                     score: float) -> None:
        """
        Logs the results of a processor evaluation to a file.
        :param processor_name: The name of the processor.
        :param params: The parameters used for this evaluation.
        :param time_taken: Time taken for the processing in seconds.
        :param score: The score obtained from the evaluation function.
        """
        with open(self.logfile_path, 'a') as file:
            file.write(f"Processor: {processor_name}\n")
            for param, value in params.items():
                file.write(f"{param}: {value}\n")
            file.write(f"Time Taken: {time_taken * 1000:.2f} ms\n")
            file.write(f"Score: {score}\n\n")
