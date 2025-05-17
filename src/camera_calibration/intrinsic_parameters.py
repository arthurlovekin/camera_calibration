from dataclasses import dataclass
import numpy as np
from camera_calibration.enums import CameraModel

@dataclass
class IntrinsicParameters:
    """
    Each lense has intrinsic parameters, which describe the geometry of the lense:
    focal length, principal point, and distortion coefficients. This also provides 
    a method to print out the intrinsic parameters in a readable format.
    """
    camera_model: CameraModel
    fx: float
    fy: float
    cx: float
    cy: float
    distortion_coefficients: list[float]

    def __str__(self):
        def format_mat(x, precision=5):
            return ("[%s]" % (
                np.array2string(x, precision=precision,
                                   suppress_small=True, separator=", ")
                    .replace("[", "").replace("]", "").replace("\n", "\n        ")
                    ))

        # Create camera matrix K
        k = np.array([
            [self.fx, 0, self.cx],
            [0, self.fy, self.cy],
            [0, 0, 1]
        ])

        # Create identity matrices for R and P
        r = np.eye(3)
        p = np.array([
            [self.fx, 0, self.cx, 0],
            [0, self.fy, self.cy, 0],
            [0, 0, 1, 0]
        ])

        # Convert distortion coefficients to np array
        d = np.array(self.distortion_coefficients)

        # Get distortion model based on camera model
        dist_model = "plumb_bob" if self.camera_model == CameraModel.PINHOLE else "equidistant"

        return "\n".join([
            "camera_matrix:",
            "  rows: 3",
            "  cols: 3",
            "  data: " + format_mat(k),
            "distortion_model: " + dist_model,
            "distortion_coefficients:",
            "  rows: 1",
            "  cols: %d" % len(self.distortion_coefficients),
            "  data: [%s]" % ", ".join("%8f" % x for x in d.flat),
            "rectification_matrix:",
            "  rows: 3",
            "  cols: 3",
            "  data: " + format_mat(r, 8),
            "projection_matrix:",
            "  rows: 3",
            "  cols: 4",
            "  data: " + format_mat(p),
            ""
        ])


