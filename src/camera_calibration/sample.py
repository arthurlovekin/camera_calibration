"""
A Sample contains
1. The raw data of the image(s) and any additional data (eg. pose for extrinsic calibration)
2. The processed points that were detected in the image(s)
"""
from dataclasses import dataclass
import numpy as np

@dataclass
class MonoSample:
    image: np.ndarray
    pixel_points: np.ndarray # 2D points in the image
    world_points: np.ndarray # Scaled 3D points from the target

@dataclass
class StereoSample(Sample):
    left_image: np.ndarray
    right_image: np.ndarray
    left_pixel_points: np.ndarray
    right_pixel_points: np.ndarray
    world_points: np.ndarray


@dataclass
class HandEyeSample(Sample):
    image: np.ndarray
    pixel_points: np.ndarray
    world_points: np.ndarray
    pose: np.ndarray
