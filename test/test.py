import cv2
import argparse
from camera_calibration.calibrator import IntrinsicCalibrator, StereoCalibrator, HandEyeCalibrator
from camera_calibration.enums import CalibrationMode, PatternType, CameraModel

def parse_arguments():
    parser = argparse.ArgumentParser(description='Camera Calibration Tool')
    
    # Calibration mode
    parser.add_argument('--calibration-mode', type=str, choices=[e.value for e in CalibrationMode], 
                        default=CalibrationMode.INTRINSIC.value,
                        help=f'Calibration mode: {", ".join([e.value for e in CalibrationMode])}')
    
    # Camera type
    parser.add_argument('--camera-model', type=str, choices=[e.value for e in CameraModel],
                        default=CameraModel.PINHOLE.value,
                        help=f'Camera model: {", ".join([e.value for e in CameraModel])}')
    
    # Pattern type and properties
    parser.add_argument('--pattern', type=str, choices=[e.value for e in PatternType],
                        default=PatternType.CHESSBOARD.value,
                        help=f'Calibration pattern type: {", ".join([e.value for e in PatternType])}')
    parser.add_argument('--rows', type=int, default=6,
                        help='Number of rows in the pattern')
    parser.add_argument('--columns', type=int, default=8,
                        help='Number of columns in the pattern')
    parser.add_argument('--square-size-mm', type=float, default=10,
                        help='Square size of the pattern in millimeters (this means different things for different patterns; see gen_pattern.py)')
    
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

def initialize_calibrator(args):
    if args.calibration_mode == CalibrationMode.INTRINSIC.value:
        calibrator = Calibrator(args)
    elif args.calibration_mode == CalibrationMode.STEREO.value:
        calibrator = StereoCalibrator(args)
    elif args.calibration_mode == CalibrationMode.HAND_EYE.value:
        calibrator = HandEyeCalibrator(args)
    return calibrator

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
