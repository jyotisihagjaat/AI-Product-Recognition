import random, shutil
from ultralytics import YOLO
from labels import PRODUCTS
from config import ROOT, IMG_SIZE

RAW, DATA = ROOT/"raw_images", ROOT/"dataset"

def main():
    # Check every class before touching dataset/, so a failed check leaves it intact.
    short = []
    for _, name, folder, _ in PRODUCTS:
        count = len(list((RAW/folder).glob("*.jpg")))
        if count < 10:
            short.append((name, count))
    if short:
        for name, count in short:
            print(f"{name}: only {count} photos. Capture at least 10; aim for 30-50.")
        print(f"{len(short)} product(s) need more photos. Run src\\collect_data.py, then train again.")
        return
    if DATA.exists():
        shutil.rmtree(DATA)
    random.seed(42)
    for _, name, folder, _ in PRODUCTS:
        images = list((RAW/folder).glob("*.jpg"))
        random.shuffle(images)
        nval = max(2, int(len(images)*.2))
        for split, group in (("train", images[nval:]), ("val", images[:nval])):
            dest = DATA/split/folder
            dest.mkdir(parents=True, exist_ok=True)
            for i, img in enumerate(group):
                shutil.copy2(img, dest/f"{i:04d}.jpg")
        print(f"{name}: {len(images)-nval} train, {nval} validation")
    print("Loading small YOLO11n classification model. First run downloads weights.")
    model = YOLO("yolo11n-cls.pt")
    model.train(data=str(DATA), epochs=20, imgsz=IMG_SIZE, batch=16,
                device="cpu", workers=0, patience=5,  # GPU users may change device, e.g. device=0
                project=str(ROOT/"runs"), name="product_classifier", exist_ok=True)
    print("Training complete. Double-click run.bat (or run src\\recognize.py).")

if __name__ == "__main__":
    main()
