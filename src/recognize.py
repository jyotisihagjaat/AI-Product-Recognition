import sys
import time
import cv2
from ultralytics import YOLO
from config import (MODEL_PATH, CAMERA_INDEX, CROP_RATIO, IMG_SIZE, CONF_THRESHOLD,
                    MAX_READ_FAILURES, BOX_COLOR, center_square, label_text)
from labels import DISPLAY_NAMES


def main():
    if not MODEL_PATH.exists():
        print(f"No trained model found at {MODEL_PATH}.")
        print("Collect photos and train first:")
        print(r"  1) .\.venv\Scripts\python.exe src\collect_data.py")
        print(r"  2) .\.venv\Scripts\python.exe src\train_model.py")
        return 2

    print("Loading AI model...")
    model = YOLO(str(MODEL_PATH))
    print("Model loaded successfully!")
    print(f"Unknown threshold: {CONF_THRESHOLD * 100:.0f}% (edit CONF_THRESHOLD in src/config.py)")

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Camera not found. Close other camera apps or change CAMERA_INDEX in src/config.py.")
        return 1

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    print("Camera started! Press Q to quit.")
    failures = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                failures += 1
                time.sleep(0.05)
                if failures >= MAX_READ_FAILURES:
                    print("Lost the camera feed.")
                    return 1
                continue
            failures = 0

            # Classify the same centred square that collect_data.py saved for training.
            h, w = frame.shape[:2]
            x1, y1, x2, y2 = center_square(h, w, CROP_RATIO)
            crop = frame[y1:y2, x1:x2]
            result = model.predict(source=crop, imgsz=IMG_SIZE, verbose=False)[0]
            folder = model.names[result.probs.top1]
            conf = float(result.probs.top1conf)
            label = label_text(DISPLAY_NAMES.get(folder, folder), conf, CONF_THRESHOLD)

            cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
            cv2.rectangle(frame, (10, 10), (w - 10, 85), (20, 20, 20), -1)
            cv2.putText(
                frame, label, (25, 58),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                (0, 255, 100), 2
            )

            cv2.imshow("AI Product Recognition", frame)

            if (cv2.waitKey(1) & 0xFF) in (ord("q"), ord("Q")):
                break
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    sys.exit(main())
