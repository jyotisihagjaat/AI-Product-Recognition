import pytest
from config import center_square, next_image_number, label_text


@pytest.mark.parametrize("h, w, expected", [
    (480, 640, (133, 53, 507, 427)),
    (720, 1280, (359, 79, 920, 640)),
    (640, 480, (53, 133, 427, 507)),
    (1080, 1920, (539, 119, 1381, 961)),
])
def test_center_square_values(h, w, expected):
    x1, y1, x2, y2 = center_square(h, w, 0.78)
    assert (x1, y1, x2, y2) == expected
    assert x2 - x1 == y2 - y1


def original_crop(h, w):
    # Inline formula from the original collect_data.py
    side = int(min(h, w) * 0.78)
    x1, y1 = (w-side)//2, (h-side)//2
    return (x1, y1, x1+side, y1+side)


def test_center_square_matches_original_formula():
    for h in range(100, 2000, 37):
        for w in range(100, 2000, 37):
            assert center_square(h, w, 0.78) == original_crop(h, w)


@pytest.mark.parametrize("stems, expected", [
    (["0001", "0003", "0005"], 6),
    ([], 1),
    (["0001", "notes", "IMG_12", "0002 copy"], 2),
    (["9999"], 10000),
])
def test_next_image_number(stems, expected):
    assert next_image_number(stems) == expected


def test_next_image_number_generator():
    assert next_image_number(s for s in ["0002", "0004"]) == 5


def test_label_text():
    assert label_text("Body Lotion", 0.91, 0.60) == "Body Lotion | 91.0%"
    assert label_text("Cup", 0.42, 0.60) == "Unknown | 42.0%"
    assert label_text("Cup", 0.60, 0.60) == "Cup | 60.0%"
