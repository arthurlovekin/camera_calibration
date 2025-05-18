import cv2
from camera_calibration.cli import create_calibrator
from camera_calibration.sample import MonoSample

def main():
    print(f"You are using OpenCV version {cv2.__version__}")
    calibrator = create_calibrator()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        sample = MonoSample(frame)
        calibrator.maybe_add_sample(sample)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
