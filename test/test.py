import cv2
import argparse
import numpy as np
from enum import Enum
from camera_calibration.calibrator import Calibrator


class CalibrationMode(Enum):
    INTRINSIC = 'intrinsic'
    EXTRINSIC = 'extrinsic'


class CameraType(Enum):
    MONOCULAR = 'mono'
    STEREO = 'stereo'


class TargetType(Enum):
    CHESSBOARD = 'chessboard'
    ACIRCLES = 'acircles'


def parse_arguments():
    parser = argparse.ArgumentParser(description='Camera Calibration Tool')
    
    # Calibration mode
    parser.add_argument('--mode', type=str, choices=[e.value for e in CalibrationMode], 
                        default=CalibrationMode.INTRINSIC.value,
                        help='Calibration mode: intrinsic or extrinsic')
    
    # Camera type
    parser.add_argument('--camera', type=str, choices=[e.value for e in CameraType],
                        default=CameraType.MONOCULAR.value,
                        help='Camera type: mono or stereo')
    
    # Pattern type and properties
    parser.add_argument('--pattern', type=str, choices=[e.value for e in TargetType],
                        default=TargetType.CHESSBOARD.value,
                        help='Calibration pattern type: chessboard or acircles')
    parser.add_argument('--rows', type=int, default=6,
                        help='Number of rows in the pattern')
    parser.add_argument('--columns', type=int, default=8,
                        help='Number of columns in the pattern')
    parser.add_argument('--square-size-mm', type=float, default=10,
                        help='Square size in millimeters for chessboard pattern')
    
    # Additional options
    parser.add_argument('--approximate', type=float, default=0.0,
                        help='Allow specified slop (in seconds) when pairing images from unsynchronized stereo cameras')
    parser.add_argument('--k-coefficients', type=int, default=2,
                        help='Number of radial distortion coefficients to use')
    parser.add_argument('--fix-principal-point', action='store_true',
                        help='Fix the principal point at the center')
    parser.add_argument('--fix-aspect-ratio', action='store_true',
                        help='Fix the aspect ratio')
    
    return parser.parse_args()


def main():
    print(f"You are using OpenCV version {cv2.__version__}")
    cap = cv2.VideoCapture(0)
    args = parse_arguments()
    calibrator = Calibrator(args)

    while True:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
