from camera_calibration.calibrator import Calibrator, IntrinsicCalibrator, StereoCalibrator, HandEyeCalibrator
from camera_calibration.enums import CalibrationMode, PatternType, CameraModel
from camera_calibration.pattern import Chessboard, AcirclesGrid
import argparse
class PatternAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        if not hasattr(namespace, 'patterns'):
            namespace.patterns = []
        
        # Get the corresponding parameters for this pattern
        if not hasattr(namespace, 'current_rows'):
            namespace.current_rows = None
        if not hasattr(namespace, 'current_columns'):
            namespace.current_columns = None
        if not hasattr(namespace, 'current_square_size'):
            namespace.current_square_size = None
            
        # Validate that all required parameters are present
        if namespace.current_rows is None:
            parser.error(f"Pattern {values} requires --rows")
        if namespace.current_columns is None:
            parser.error(f"Pattern {values} requires --columns")
        if namespace.current_square_size is None:
            parser.error(f"Pattern {values} requires --square-size-mm")
        
        # Validate that the pattern has at least 2 rows and columns
        if namespace.current_rows < 2:
            parser.error(f"Pattern {values} requires at least 2 rows")
        if namespace.current_columns < 2:
            parser.error(f"Pattern {values} requires at least 2 columns")
        if namespace.current_square_size <= 0:
            parser.error(f"Pattern {values} requires a positive square size")
            
        # Create and store the pattern based on type
        if values == PatternType.CHESSBOARD.value:
            pattern = Chessboard(
                n_rows=namespace.current_rows,
                n_cols=namespace.current_columns,
                square_size=namespace.current_square_size
            )
        elif values == PatternType.ACIRCLES.value:
            pattern = AcirclesGrid(
                n_rows=namespace.current_rows,
                n_cols=namespace.current_columns,
                square_size=namespace.current_square_size
            )
        else:
            parser.error(f"Unsupported pattern type: {values}")
            
        namespace.patterns.append(pattern)
        
        # Reset the current parameters
        namespace.current_rows = None
        namespace.current_columns = None
        namespace.current_square_size = None

def parse_arguments():
    parser = argparse.ArgumentParser(description='Camera Calibration Tool')
    
    # Calibration mode
    parser.add_argument('--calibration-mode', type=str, choices=[e.value for e in CalibrationMode], 
                        default=CalibrationMode.INTRINSIC.value,
                        help=f'Calibration mode: {", ".join([e.value for e in CalibrationMode])}')
    
    # Camera type - handled differently based on calibration mode
    parser.add_argument('--camera-model', type=str, choices=[e.value for e in CameraModel],
                        help=f'Camera model for intrinsic/hand-eye calibration, or left camera for stereo calibration: {", ".join([e.value for e in CameraModel])}')
    parser.add_argument('--right-camera-model', type=str, choices=[e.value for e in CameraModel],
                        help=f'Camera model for right camera in stereo calibration (optional, defaults to left camera model): {", ".join([e.value for e in CameraModel])}')
    
    # Pattern type and properties
    parser.add_argument('--pattern', type=str, choices=[e.value for e in PatternType],
                        action=PatternAction,
                        help=f'Calibration pattern type: {", ".join([e.value for e in PatternType])}')
    parser.add_argument('--rows', type=int, dest='current_rows',
                        help='Number of rows in the pattern')
    parser.add_argument('--columns', type=int, dest='current_columns',
                        help='Number of columns in the pattern')
    parser.add_argument('--square-size-mm', type=float, dest='current_square_size',
                        help='Square size of the pattern in millimeters')
    
    # Additional options
    parser.add_argument('--approximate', type=float, default=0.0,
                        help='Allow specified slop (in seconds) when pairing images from unsynchronized stereo cameras')
    parser.add_argument('--k-coefficients', type=int, default=2,
                        help='Number of radial distortion coefficients to use')
    parser.add_argument('--fix-principal-point', action='store_true',
                        help='Fix the principal point at the center')
    parser.add_argument('--fix-aspect-ratio', action='store_true',
                        help='Fix the aspect ratio')
    
    args = parser.parse_args()
    
    # Validate camera model arguments based on calibration mode
    if args.calibration_mode == CalibrationMode.STEREO.value:
        if args.camera_model is None:
            parser.error("--camera-model is required for stereo calibration")
        # Convert string to enum
        args.camera_model = CameraModel(args.camera_model)
        if args.right_camera_model:
            args.right_camera_model = CameraModel(args.right_camera_model)
    else:
        if args.camera_model is None:
            parser.error("--camera-model is required")
        if args.right_camera_model:
            parser.error("--right-camera-model can only be used with stereo calibration")
        # Convert string to enum
        args.camera_model = CameraModel(args.camera_model)
    
    if args.calibration_mode == CalibrationMode.HAND_EYE.value:
        # TODO: if the pattern has rotational symmetry, then we'll have problems
        pass

    # Final validation to ensure the last pattern is complete
    if hasattr(args, 'current_rows') or hasattr(args, 'current_columns') or hasattr(args, 'current_square_size'):
        parser.error("Incomplete pattern parameters. Each --pattern must be followed by --rows, --columns, and --square-size-mm")
    
    return args

def create_calibrator(args) -> Calibrator:
    if args.calibration_mode == CalibrationMode.INTRINSIC.value:
        calibrator = IntrinsicCalibrator(args.camera_model)
    elif args.calibration_mode == CalibrationMode.STEREO.value:
        calibrator = StereoCalibrator(args.camera_model, args.right_camera_model)
    elif args.calibration_mode == CalibrationMode.HAND_EYE.value:
        calibrator = HandEyeCalibrator(args.camera_model)
    return calibrator