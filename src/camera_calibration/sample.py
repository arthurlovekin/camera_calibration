"""
A Sample contains
1. The raw data of the image(s) and any additional data (eg. pose for extrinsic calibration)
2. The processed points that were detected in the image(s)
"""
class Sample:
    def __init__(self, image, points):
        self.image = image
        self.points = points


class StereoSample(Sample):
    def __init__(self, left_image, right_image):
        super().__init__(left_image, right_image)


class ExtrinsicSample(Sample):
    def __init__(self, image, points, pose):
        super().__init__(image, points)
        self.pose = pose
        
