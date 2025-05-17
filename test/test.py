import cv2
from camera_calibration.cli import parse_arguments, create_calibrator

def main():
    print(f"You are using OpenCV version {cv2.__version__}")
    cap = cv2.VideoCapture(0)
    args = parse_arguments()
    calibrator = create_calibrator(args)

    while True:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
