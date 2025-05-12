import cv2
import numpy as np
from abc import ABC, abstractmethod
from lense import Lense
from sample import MonoSample, StereoSample, HandEyeSample

class Calibrator(ABC):
    """
    A calibrator manages the collection of samples, 
    calculating the distribution of the samples to determine when the calibration is ready to run, 
    running the calibration itself, 
    and saving the samples and calibration output to a file.
    """
    def __init__(self):
        self.samples = []
        self.n_points = 0

        # distribution requirements
        self.min_n_points = 500 # the minimum number of image points
        self.min_n_points_per_bin = 3 # the minimum number of points in each bin
        self.min_scale_range_px = 100 # the difference between the span of the smallest and largest samples in the image 
        self.min_skew_range_deg = 10 # the difference between the angle of the smallest and largest samples in the image
        self.xy_bin_count = np.zeros((2,3)) # 2D histogram of the x and y coordinates of the samples
        # TODO: resize the number of bins to be a function of the image size
    
    @abstractmethod
    def maybe_add_sample(self, sample):
        """
        Adds a sample to the calibrator if it improves the distribution of the samples.
        """
        pass

    @abstractmethod
    def distribution_is_good(self):
        """
        Checks that there are:
        - at least 500 image points (~10 samples depending on the pattern size)
        - more than 3 points in each region of the image (good x/y distribution)
        - samples with a diversity of distances from the camera (small and large in the image)
        - samples with a diversity of angles to the camera (skewed in the image)
        """
        pass

    @abstractmethod
    def calibrate(self, force=False):
        """
        Runs the OpenCV camera calibration function.
        If force is True, the calibration will run even if the distribution is not good.
        """
        pass

    @abstractmethod
    def print_calibration_results(self):
        """
        Prints the calibration results to the terminal in a readable format.
        """
        pass

    @abstractmethod
    def save_calibration_results(self, file_path):
        """
        Saves the calibration results to a folder.
        """
        pass


class MonoCalibrator(Calibrator):

    def maybe_add_sample(self, sample: MonoSample):
        """
        Adds a sample to the calibrator if it improves the distribution of the samples.
        """
        pass

    def distribution_is_good(self):
        if self.n_points < self.min_n_points:
            return False
        
        if np.any(self.xy_bin_count < self.min_n_points_per_bin):
            return False
        
        # check that the samples are spread out enough
        if(self.min_scale_range_px is not None and 
           self.xy_bin_count[0,2] < self.min_scale_range_px):
            return False
        
        if(self.min_skew_range_deg is not None and 
           self.xy_bin_count[1,2] < self.min_skew_range_deg):
            return False
        
        return True
    
    def calibrate(self, force=False):
        """
        Runs the calibration
        """
        if force:
            print("Warning: the distribution of samples is not good enough to guarantee good calibration results")
        elif not self.distribution_is_good():
            print("The distribution of samples is not good, skipping calibration")
            return
        
        print("Calibrating...")
        # Extract object points and image points from samples
        object_points = []  # 3D points in real world space
        image_points = []   # 2D points in image plane
        
        for sample in self.samples:
            # Convert world_points to numpy array for object points
            obj_pts = np.array([point.coordinates for point in sample.world_points], dtype=np.float32)
            object_points.append(obj_pts)
            
            # Convert pixel_points to numpy array for image points
            img_pts = np.array([point.coordinates for point in sample.pixel_points], dtype=np.float32)
            image_points.append(img_pts)
        
        # Initialize camera matrix if not already set
        if self.camera.camera_matrix is None:
            self.camera.camera_matrix = np.zeros((3, 3), dtype=np.float32)
            self.camera.camera_matrix[0, 0] = 1.0  # Initial guess for fx
            self.camera.camera_matrix[1, 1] = 1.0  # Initial guess for fy
            self.camera.camera_matrix[0, 2] = self.camera.image_width / 2   # Initial guess for cx
            self.camera.camera_matrix[1, 2] = self.camera.image_height / 2  # Initial guess for cy
            self.camera.camera_matrix[2, 2] = 1.0
        
        # Initialize distortion coefficients if not already set
        if self.camera.dist_coeffs is None:
            self.camera.dist_coeffs = np.zeros(5, dtype=np.float32)
        
        # Run calibration and get results
        ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
            objectPoints=object_points,
            imagePoints=image_points,
            imageSize=(self.camera.image_width, self.camera.image_height),
            cameraMatrix=self.camera.camera_matrix,
            distCoeffs=self.camera.dist_coeffs,
        )
        

class StereoCalibrator(Calibrator):
    def __init__(self):
        super().__init__()
        self.left_calibrator = MonoCalibrator()
        self.right_calibrator = MonoCalibrator()
    
    def maybe_add_sample(self, sample: StereoSample):
        """
        Adds a sample to the calibrator if it improves the distribution of the samples.
        """
        # If only one image is present (because the sample is out of view of one camera),
        # then only add the sample to the calibrator that has the image.
        if sample.left_image is None:
            mono_sample = MonoSample(sample.world_points, sample.right_image)
            self.right_calibrator.maybe_add_sample(mono_sample)
        elif sample.right_image is None:
            mono_sample = MonoSample(sample.world_points, sample.left_image)
            self.left_calibrator.maybe_add_sample(mono_sample)
        else:
            mono_sample_left = MonoSample(sample.world_points, sample.left_image)
            mono_sample_right = MonoSample(sample.world_points, sample.right_image)
            self.left_calibrator.maybe_add_sample(mono_sample_left)
            self.right_calibrator.maybe_add_sample(mono_sample_right)
            self.samples.append(sample)

    def distribution_is_good(self):
        return self.left_calibrator.distribution_is_good() and self.right_calibrator.distribution_is_good()
    
    def calibrate(self, force=False):
        """
        Runs the calibration
        """
        if force:
            print("Warning: the distribution of samples is not good enough to guarantee good calibration results")
        elif not self.distribution_is_good():
            print("The distribution of samples is not good, skipping calibration")
            return
        
        print("Calibrating...")
        # First perform an intrinsic calibration for each camera
        K_left, dist_coeffs_left = self.left_calibrator.calibrate()
        K_right, dist_coeffs_right = self.right_calibrator.calibrate()

        # Then perform a stereo calibration
        ret, K_left, K_right, R, t, E, F = cv2.stereoCalibrate(
            objectPoints=object_points,
            imagePoints1=image_points1,
            imagePoints2=image_points2,
            imageSize=(self.camera.image_width, self.camera.image_height),
            cameraMatrix1=K_left,
            distCoeffs1=dist_coeffs_left,
            cameraMatrix2=K_right,
            distCoeffs2=dist_coeffs_right,
            flags=cv2.CALIB_FIX_INTRINSIC,
        )
        

class HandEyeCalibrator(Calibrator):
    def __init__(self):
        super().__init__()
        self.mono_calibrator = MonoCalibrator()
    
    def maybe_add_sample(self, sample: HandEyeSample):
        """
        Adds a sample to the calibrator if it improves the distribution of the samples.
        """
        pass
    
    def distribution_is_good(self):
        return self.mono_calibrator.distribution_is_good()
    
    def calibrate(self, force=False):
        """
        Runs the calibration
        """
        if force:
            print("Warning: the distribution of samples is not good enough to guarantee good calibration results")
        elif not self.distribution_is_good():
            print("The distribution of samples is not good, skipping calibration")
            return
        
        print("Calibrating...")
        # First perform the intrinsic calibration 
        K, dist_coeffs, rvecs, tvecs = self.mono_calibrator.calibrate()

        # Then perform the hand-eye calibration
        ret, rvec, tvec = cv2.calibrateHandEye(
            rvecs=rvecs,
            tvecs=tvecs,
            R=R,
            T=t,
            method=cv2.CALIB_HAND_EYE_TSAI,
        )
