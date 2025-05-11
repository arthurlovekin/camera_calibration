import cv2
from camera_calibration import Pattern, Camera

# TODO: rename SampleDistributionManager
class Calibrator:
    """
    A calibrator manages the collection of samples, 
    calculating the distribution of the samples to determine when the calibration is ready to run, 
    running the calibration itself, 
    and saving the samples and calibration output to a file.
    """
    def __init__(self, camera: Camera, patterns: Pattern | list[Pattern]):
        self.samples = []
        self.n_image_points = 0
        if isinstance(patterns, Pattern):
            self.patterns = [patterns]
        else:
            self.patterns = patterns
    
    def add_sample(self, sample):
        self.samples.append(sample)
        self.n_image_points += len(sample.image_points)
        if self._distribution_is_good():
            self.distribution_is_good = True
        

    def _distribution_is_good(self):
        """
        Checks that there are:
        - at least 500 image points (~10 samples depending on the pattern size)
        - more than 3 points in each region of the image (good x/y distribution)
        - samples with a diversity of distances from the camera (small and large in the image)
        - samples with a diversity of angles to the camera (skewed in the image)
        """
        if self.n_image_points < 500:
            return False
        return True
    
    def force_calibration(self):
        self.distribution_is_good = True
        print("Warning: The distribution of samples is not yet good enough to ensure accurate results")
        self.calibrate()
    
    def calibrate(self):
        """
        Runs the calibration
        """
        if not self.distribution_is_good:
            print("The distribution of samples is not good, skipping calibration")
            return
        
        print("Calibrating...")
        self.camera.calibrate()
        self.camera.save_calibration()

        cv2.calibrateCamera(
            objectPoints=self.samples,
            imagePoints=self.samples,
            imageSize=(self.camera.image_width, self.camera.image_height),
            cameraMatrix=self.camera.camera_matrix,
            distCoeffs=self.camera.dist_coeffs,
        )
        


        
        
        

