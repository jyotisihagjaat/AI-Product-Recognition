import re
from pathlib import Path
from labels import PRODUCTS, PROMPTS, DISPLAY_NAMES

ORIGINAL_V1_PROMPTS = [
    "smartphone", "phone charger", "bangle bracelet", "body lotion bottle",
    "lip gloss tube", "spoon", "Bournvita drink container", "packaged snack packet",
    "notebook", "pen", "glue bottle", "drinking cup", "water bottle",
]


def test_products_shape():
    assert len(PRODUCTS) == 13
    keys = [p[0] for p in PRODUCTS]
    assert keys == list("abcdefghijklm")
    folders = [p[2] for p in PRODUCTS]
    assert len(set(folders)) == 13
    assert all(re.fullmatch(r"[a-z_]+", f) for f in folders)
    assert all(len(p) == 4 and p[3] for p in PRODUCTS)


def test_display_names():
    assert DISPLAY_NAMES["body_lotion"] == "Body Lotion"


def test_prompts_match_v1():
    assert PROMPTS == ORIGINAL_V1_PROMPTS


def test_v1_has_no_product_literals():
    src = (Path(__file__).resolve().parents[1] / "src" / "product_detector.py").read_text(encoding="utf-8")
    assert not any(f'"{p}"' in src for p in ORIGINAL_V1_PROMPTS)
