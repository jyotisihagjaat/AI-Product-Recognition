# Legacy V1 (YOLO-World). The default app is V2: collect_data.py -> train_model.py -> recognize.py.
import sys
import cv2
from ultralytics import YOLOWorld
from labels import PRODUCTS, PROMPTS
from config import CAMERA_INDEX

# ---------------------------------------------------------
# AI PRODUCT RECOGNITION SYSTEM
# ---------------------------------------------------------

MODEL_NAME = "yolov8s-worldv2.pt"
CONFIDENCE_THRESHOLD = 0.20
IMAGE_SIZE = 640

DISPLAY_NAMES = {i: name for i, (_, name, _, _) in enumerate(PRODUCTS)}


def main():
    print("\n" + "=" * 52)
    print("          AI PRODUCT RECOGNITION SYSTEM")
    print("=" * 52)
    print("Loading YOLO-World model. First launch may take a while...")

    try:
        model = YOLOWorld(MODEL_NAME)
        model.set_classes(PROMPTS)
    except Exception as error:
        print("\nCould not load the AI model.")
        print("Check your internet connection and try again.")
        print(f"Details: {error}")
        input("\nPress Enter to close...")
        return

    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print("\nCould not open the webcam.")
        print("Close other camera apps or change CAMERA_INDEX in src/config.py.")
        input("\nPress Enter to close...")
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("\nCamera started!")
    print("Show one product at a time. Press Q in the camera window to quit.")

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Could not read a frame from the webcam.")
                break

            # Run open-vocabulary object detection on the current frame.
            results = model.predict(
                source=frame,
                conf=CONFIDENCE_THRESHOLD,
                imgsz=IMAGE_SIZE,
                verbose=False
            )

            # Add a clean header to the live camera view.
            display = frame.copy()
            cv2.rectangle(display, (0, 0), (display.shape[1], 58), (25, 25, 25), -1)
            cv2.putText(
                display,
                "AI PRODUCT RECOGNITION",
                (20, 38),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            detected_names = []

            if results and results[0].boxes is not None:
                boxes = results[0].boxes

                for box in boxes:
                    class_id = int(box.cls[0].item())
                    confidence = float(box.conf[0].item())

                    if class_id not in DISPLAY_NAMES:
                        continue

                    name = DISPLAY_NAMES[class_id]
                    detected_names.append(name)

                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    label = f"{name}  {confidence * 100:.0f}%"

                    # Draw detection box and label.
                    cv2.rectangle(display, (x1, y1), (x2, y2), (40, 220, 120), 2)
                    label_y = max(y1 - 10, 75)
                    cv2.rectangle(
                        display,
                        (x1, label_y - 28),
                        (x1 + max(150, len(label) * 12), label_y + 4),
                        (40, 220, 120),
                        -1
                    )
                    cv2.putText(
                        display,
                        label,
                        (x1 + 6, label_y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (15, 25, 20),
                        2,
                        cv2.LINE_AA
                    )

            # Show the current result in a fixed bottom panel.
            if detected_names:
                unique_names = list(dict.fromkeys(detected_names))
                result_text = "Detected: " + ", ".join(unique_names[:3])
            else:
                result_text = "Detected: Looking for a product..."

            panel_y = display.shape[0] - 52
            cv2.rectangle(
                display,
                (0, panel_y),
                (display.shape[1], display.shape[0]),
                (25, 25, 25),
                -1
            )
            cv2.putText(
                display,
                result_text[:100],
                (20, panel_y + 34),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            cv2.imshow("AI Product Recognition - Press Q to Quit", display)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nStopping camera...")
    except Exception as error:
        print(f"\nAn unexpected error occurred: {error}")
    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("\nCamera closed. Thank you for using the project!")


if __name__ == "__main__":
    main()
