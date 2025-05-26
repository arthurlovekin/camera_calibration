### Camera Calibration
This is a package for intrinsic and extrinsic camera calibration. This package wraps the [OpenCV Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.5.4/d9/d0c/group__calib3d.html#ga93efa9b0aa890de240ca32b11253dd4a) module ([github](https://github.com/opencv/opencv/tree/4.x/modules/calib3d)) in order to provide
1. Accurate intrinsic (mono), stereo, and extrinsic (hand-eye) calibration, along with error metrics
2. A data collection method that is standard across these different types of calibrations (which hopefully makes the code easier to read). You can feed images in real-time or calibrate from a tar file.
3. A simple but configurable graphical user interface 

This package provides similar functionality to the [ROS2 image-pipeline camera_calibration](https://github.com/ros-perception/image_pipeline/tree/rolling/camera_calibration) package, but does not have the ROS2 dependency. As such, this package does not provide a way to capture the image frames which are needed as input.

## Quick Start
Print out one of the default patterns in the `pattern` directory and attach it to a rigid flat surface.

Run the camera calibration script:

Once you've collected sufficient samples and clicked "Calibrate," the output files are saved to the  the calibrate button will become available. 

## Camera Calibration Overview
Step 1 is always to do the intrinsic calibration (detect image points, get a good distribution, then calibrate)
Stereo takes the intrinsic calibration of 2 cameras and finds the pose of one wrt the other
Extrinsic uses the calibration above + solvePnP in order to find camera_wrt_target. Additionally, collect robot poses.

Arguably the radon board or charuco should be used for all three steps (other boards fall short because it isn't as easy to estimate the full pose of the target wrt camera).

# Intrinsic Camera Calibration (monocular)
Calculate the intrinsic parameters of a single camera lense. This includes the focal lengths (fx, fy) and image center point (cx,cy), which together make up the intrinsic camera matrix (denoted K). This also includes the 5 distortion coefficients of the pinhole camera model (denoted D).
This wraps OpenCV's calibrateCamera() function.

# Stereo Camera Calibration 
This will first perform an intrinsic camera calibration for both lenses, then 
This wraps openCV's [stereoCalibrate()](https://docs.opencv.org/4.5.4/d9/d0c/group__calib3d.html#ga246253dcc6de2e0376c599e7d692303a) function

# Extrinsic (Hand-Eye) Calibration
This wraps openCV's [calibrateHandEye()](https://docs.opencv.org/4.5.4/d9/d0c/group__calib3d.html#gaebfc1c9f7434196a374c382abf43439b) function.

It is recommended to use the RadonCheckerboard as it is easier to detect and results in less reprojection error compared to chessboard and acircles grid.
For extrinsic hand-eye calibration, you need to choose a pattern that has no rotational symmetry. For example, a chessboard with an odd number of columns and rows is good, but if there are an even number of columns and rows then there is no way to distinguish 0 and 180 degree rotations. (TODO: enforce this in the generation and initialization script)

The corner detection algorithms will always try to detect interior corners (points that lies at the intersection of two black and two white squares). For example, a chessboard with 8 squares per row and 5 squares per column will have 7 interior points per row and 4 interior points per column, and the detection algorithm will find 28 points total.

## Generate your own pattern

[OpenCV Instructions](https://docs.opencv.org/4.x/da/d0d/tutorial_camera_calibration_pattern.html)
[OpenCV Source Code](https://github.com/opencv/opencv/blob/4.x/doc/pattern_tools/gen_pattern.py)

Example:
```
python pattern/gen_pattern.py -o radon_checkerboard.svg --rows 10 --columns 15 --type radon_checkerboard -s 12.1 -m 7 4 7 5 8 5
```
Use Inkscape or Adobe Illustrator to open the SVG file, add text description, and convert to PNG to print.

## Architecture design
One thing about OpenCV is that they provide a lot of options, some of which are strictly superior to others. Part of the goal in this repo is to only support the best options, so that by default the user can perform a highly accurate calibration without needing to make decisions and reading the literature.
As of now


## Tips
Be Careful with your OpenCV version! Between versions 3 and 4 they randomly decided to switch function arguments around, so always check that the docs you're reading online correspond to the version you're using.