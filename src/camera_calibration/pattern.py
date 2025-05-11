import cv2
from abc import ABC, abstractmethod

class Pattern(ABC):
    """
    A physical object of known dimensions that you wave in front of 
    a camera to collect sample points. For example, a chessboard or an asymmetric circle grid.
    Each Pattern has an associated function that OpenCV uses to detect the points, as well as 
    a method to draw the pattern on an image.
    """
    def __init__(self, height, width, square_size):
        self.height = height
        self.width = width
        self.square_size = square_size

    @abstractmethod
    def detect_points(self, image):
        pass

    # TODO: should this method be here, or since it is drawing points is it ok to put it somewhere else?
    # For now I'll keep it here, because theoretically it seems like there could be patterns that are not grids.
    def draw(self, image, corners, ret):
        cv2.drawChessboardCorners(image, (self.width, self.height), corners, ret)

class RadonCheckerboard(Pattern):
    def __init__(self, height, width, square_size):
        super().__init__(height, width, square_size)

    def detect_points(self, image):
        return cv2.findChessboardCornersSB(image, (self.width, self.height), None)
    
class Chessboard(Pattern):
    def __init__(self, height, width, square_size):
        super().__init__(height, width, square_size)
        raise NotImplementedError("Chessboard is not implemented yet")

    def detect_points(self, image):
        # TODO: Add sub-pixel detection as in image_pipeline
        return cv2.findChessboardCorners(image, (self.width, self.height), None)
    
    def draw(self, image, corners, ret):
        return cv2.drawChessboardCorners(image, (self.width, self.height), corners, ret)

class AcirclesGrid(Pattern):
    def __init__(self, height, width, square_size):
        super().__init__(height, width, square_size)
        raise NotImplementedError("AcirclesGrid is not implemented yet")

    def detect_points(self, image):
        return cv2.findAcirclesGrid(image, (self.width, self.height), None)
    
    def draw(self, image, corners, ret):
        return cv2.drawChessboardCorners(image, (self.width, self.height), corners, ret)
