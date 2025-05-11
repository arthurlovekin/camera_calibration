"""
Each lense has intrinsic parameters, which describe the geometry of the lense:
focal length, principal point, and distortion coefficients.

A monocular camera has one lense, a stereo camera has two.
The extrinsic parameters (which describe the camera's pose with respect to the world)
are stored in the camera object.
"""
from enum import Enum

class CameraModel(Enum):
    PINHOLE = "pinhole"
    FISHEYE = "fisheye"

class Lense:
    def __init__(self):
        self.camera_model = CameraModel.PINHOLE
        self.calibrated = False

        # intrinsic parameters
        self.fx = None
        self.fy = None
        self.cx = None
        self.cy = None
        self.distortion_coefficients = [None]*5


    def __str__(self):
        return f"Lense(intrinsic_parameters={self.intrinsic_parameters}, extrinsic_parameters={self.extrinsic_parameters})"


