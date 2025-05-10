"""
A Target is a calibration board of known dimensions that you wave in front of 
a camera to collect sample points. For example, a checkerboard or an asymmetric circle grid.
Each Target has an associated function that OpenCV uses to detect the points.
"""
import cv2
from abc import ABC, abstractmethod

class Target(ABC):
    def __init__(self, height, width, square_size):
        self.height = height
        self.width = width
        self.square_size = square_size

    @abstractmethod
    def detect_points(self, image):
        pass

class Checkerboard(Target):
    def __init__(self, height, width, square_size):
        super().__init__(height, width, square_size)

    def detect_points(self, image):
        return cv2.findChessboardCorners(image, (self.width, self.height), None)

class AcirclesGrid(Target):
    def __init__(self, height, width, square_size):
        super().__init__(height, width, square_size)

    def detect_points(self, image):
        return cv2.findAcirclesGrid(image, (self.width, self.height), None)
