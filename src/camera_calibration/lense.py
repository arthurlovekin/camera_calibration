"""
Each lense has intrinsic parameters, which describe the geometry of the lense:
focal length, principal point, and distortion coefficients.

Each lense also has extrinsic parameters, which describe the camera's pose with respect to the world (or the other lense).

A monocular camera has one lense, a stereo camera has two.
"""

class Lense:
    def __init__(self, intrinsic_parameters, extrinsic_parameters):
        self.intrinsic_parameters = intrinsic_parameters
        self.extrinsic_parameters = extrinsic_parameters

    def __str__(self):
        return f"Lense(intrinsic_parameters={self.intrinsic_parameters}, extrinsic_parameters={self.extrinsic_parameters})"


