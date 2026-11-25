import cv2
from labels import PRODUCTS
from config import ROOT, CAMERA_INDEX, CROP_RATIO, BOX_COLOR, center_square, next_image_number

SAVE = ROOT / "raw_images"

def main():
    for _, _, folder, _ in PRODUCTS:
        (SAVE / folder).mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Camera not found. Close other camera apps or change CAMERA_INDEX in src/config.py.")
        return
    selected = None
    print("Press product letter A-M to select, SPACE to save, Q to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Could not read from the camera. Stopping.")
            break
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = center_square(h, w, CROP_RATIO)
        view = frame.copy()
        cv2.rectangle(view, (x1,y1), (x2,y2), BOX_COLOR, 2)
        counts = [f"{k.upper()}:{name}({len(list((SAVE/folder).glob('*.jpg')))})" for k,name,folder,_ in PRODUCTS]
        cv2.putText(view, "  ".join(counts)[:115], (10,25), cv2.FONT_HERSHEY_SIMPLEX, .45, (255,255,255), 1)
        msg = f"Selected: {selected[1]} | SPACE capture | Q quit" if selected else "Select product with A-M | Q quit"
        cv2.putText(view, msg, (10,h-15), cv2.FONT_HERSHEY_SIMPLEX, .6, (0,255,255), 2)
        cv2.imshow("Collect Product Photos", view)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), ord("Q")):
            break
        if key == 32 and selected:
            _, name, folder, _ = selected
            crop = frame[y1:y2, x1:x2]
            n = next_image_number(p.stem for p in (SAVE/folder).glob("*.jpg"))
            cv2.imwrite(str(SAVE/folder/f"{n:04d}.jpg"), crop)
            print(f"Saved {name}: {n}")
        else:
            ch = chr(key).lower() if key < 128 else ""
            match = next((p for p in PRODUCTS if p[0] == ch), None)
            if match:
                selected = match
                print(f"Selected {match[1]}. Put it in the green square and press SPACE.")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
