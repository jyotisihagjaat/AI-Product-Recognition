"""Shared settings and small pure helpers. Imports only pathlib so tests need nothing but pytest."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "runs" / "product_classifier" / "weights" / "best.pt"
CAMERA_INDEX = 0
CROP_RATIO = 0.78      # must match the crop used when photos were collected
IMG_SIZE = 160         # must match training imgsz
CONF_THRESHOLD = 0.60  # below this, show "Unknown"; tune for your setup
MAX_READ_FAILURES = 30
BOX_COLOR = (50, 220, 100)  # BGR green square


def center_square(h, w, ratio):
    """Centred square (x1, y1, x2, y2); same formula collect_data.py always used."""
    side = int(min(h, w) * ratio)
    x1, y1 = (w - side) // 2, (h - side) // 2
    return (x1, y1, x1 + side, y1 + side)


def next_image_number(stems):
    """Next free photo number: one past the highest numeric stem, so deletions never cause overwrites."""
    nums = [int(s) for s in stems if s.isdigit()]
    return max(nums) + 1 if nums else 1


def label_text(name, conf, threshold):
    shown = "Unknown" if conf < threshold else name
    return f"{shown} | {conf * 100:.1f}%"
