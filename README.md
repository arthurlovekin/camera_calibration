### Camera Calibration
This is a package for intrinsic and extrinsic camera calibration. This package wraps the [OpenCV Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.5.4/d9/d0c/group__calib3d.html#ga93efa9b0aa890de240ca32b11253dd4a) module ([github](https://github.com/opencv/opencv/tree/4.x/modules/calib3d)) in order to provide
1. Accurate camera intrinsic and extrinsic parameters, along with error metrics
2. A data collection method that is standard across different types of calibrations (which hopefully makes the code easier to read). You can feed images in real-time or calibrate from a tar file.
3. A simple but configurable graphical user interface 

This package provides similar functionality to the [ROS2 image-pipeline camera_calibration](https://github.com/ros-perception/image_pipeline/tree/rolling/camera_calibration) package, but does not have the ROS2 dependency. As such, this package does not provide a way to capture the image frames which are needed as input.

## Camera Calibration Overview

## Architecture design



## Tips
Be Careful with your OpenCV version! Between versions 3 and 4 they randomly decided to switch function arguments around, so always check that the docs you're reading online correspond to the version you're using.