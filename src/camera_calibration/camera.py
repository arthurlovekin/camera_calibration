class Camera:
    def __init__(self):
        pass

    def calibrate(self, target):
        pass

class MonoCamera(Camera):
    def __init__(self, lense):
        self.lense = lense

class StereoCamera(Camera):
    def __init__(self, left_lense, right_lense):
        self.left_lense = left_lense
        self.right_lense = right_lense

