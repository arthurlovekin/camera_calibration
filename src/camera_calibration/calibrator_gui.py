from abc import ABC, abstractmethod
import cv2
import numpy as np
from camera_calibration.calibrator import Calibrator, IntrinsicCalibrator, StereoCalibrator

class CalibratorGUI(ABC):
    def __init__(self, calibrator: Calibrator, window_name: str):
        self.calibrator = calibrator
        self.window_name = window_name

    @abstractmethod
    def show(self, sample):
        pass

    def handle_keypress(self):
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            cv2.destroyAllWindows()
            self.calibrator.close() # TODO: how does this propagate back to the CLI?
        elif key == ord('a'):
            self.calibrator.toggle_auto_collect()
        elif key == ord('c'):
            self.calibrator.calibrate()
        elif key == ord('f'):
            self.calibrator.calibrate(force=True)
        elif key == ord('s'):
            self.calibrator.save()
        elif key == ord('r'):
            self.calibrator.remove_most_recent_sample()
        elif key == ord(' '):
            if not self.calibrator.auto_collect:
                self.calibrator.collect_sample()
            else:
                print("Auto-collect is on, press [a] to turn it off. Then [spacebar] will work to collect samples.")
        else:
            self.print_instructions()

    def print_instructions(self):
        print("""
              [a] toggle auto-collect
              [c] calibrate and save the data and results
              [f] force calibration and save the data and results
              [q] or [esc] save data then quit
              [r] remove most recent sample
              [s] save raw data (and results if available)
              [spacebar] collect sample (if auto-collect is off)
              """
        )

class IntrinsicCalibratorGUI:
    def __init__(self, calibrator: IntrinsicCalibrator, window_name: str):
        super().__init__(calibrator, window_name)
    
    def show(self, sample):
        self.handle_keypress()
        cv2.imshow(self.window_name, sample.image)

class StereoCalibratorGUI:
    def __init__(self, calibrator: StereoCalibrator, window_name: str):
        super().__init__(calibrator, window_name)

    def show(self, sample):
        self.handle_keypress()
        # Create a side-by-side display of left and right images
        if sample.left_image is None and sample.right_image is None:
            print("Warning: Missing left and right image in stereo sample")
            return
        elif sample.left_image is None:
            print("Warning: Missing left image in stereo sample")
            left_img_display = np.zeros(sample.right_image.shape, dtype=np.uint8)
        elif sample.right_image is None:
            print("Warning: Missing right image in stereo sample")
            right_img_display = np.zeros(sample.left_image.shape, dtype=np.uint8)
        else:
            # both images are not None, but may differ in shape.
            # first handle difference in depth (rgb vs grayscale)
            left_dims = sample.left_image.ndim
            right_dims = sample.right_image.ndim
            if left_dims == 2 and right_dims == 2:
                left_img_display = sample.left_image
                right_img_display = sample.right_image
            elif left_dims == 3 and right_dims == 2:
                left_img_display = sample.left_image
                right_img_display = cv2.cvtColor(sample.right_image, cv2.COLOR_GRAY2BGR)
            elif left_dims == 2 and right_dims == 3:
                left_img_display = cv2.cvtColor(sample.left_image, cv2.COLOR_GRAY2BGR)
                right_img_display = sample.right_image
            else:
                raise ValueError(f"Left image dimensions: {left_dims} 
                                 and right image dimensions: {right_dims} 
                                 need to be greyscale (2) or rgb (3)")
            
        # now handle difference in shape
        def pad_to_height(img, target_height):
            pad_top = (target_height - img.shape[0]) // 2
            pad_bottom = (target_height - img.shape[0]) - pad_top
            padding = ((pad_top, pad_bottom), (0, 0)) if img.ndim == 2 else ((pad_top, pad_bottom), (0, 0), (0, 0))
            return np.pad(img, padding, mode='constant', constant_values=0)

        max_h = max(left_img_display.shape[0], right_img_display.shape[0])
        left_img_display = pad_to_height(left_img_display, max_h)
        right_img_display = pad_to_height(right_img_display, max_h)

        combined_img = np.concatenate((left_img_display, right_img_display), axis=1)

        cv2.imshow(self.window_name, combined_img)
