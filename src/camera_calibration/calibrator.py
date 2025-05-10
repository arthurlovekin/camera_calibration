"""
A calibrator manages the collection of samples, 
calculating the distribution of the samples to determine when the calibration is ready to run, 
running the calibration itself, 
and saving the samples and calibration output to a file.
"""

class Calibrator:
    def __init__(self):
        self.samples = []
        

