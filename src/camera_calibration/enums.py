from enum import Enum

class CameraModel(Enum):
    PINHOLE = "pinhole"
    FISHEYE = "fisheye"

class CalibrationMode(Enum):
    INTRINSIC = 'intrinsic'
    STEREO = 'stereo'
    HAND_EYE = 'hand_eye'

class PatternType(Enum):
    CHESSBOARD = 'chessboard'
    ACIRCLES = 'acircles'
    RADON_CHECKERBOARD = 'radon_checkerboard'