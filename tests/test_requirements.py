from pathlib import Path


def test_requirements_file():
    text = (Path(__file__).resolve().parents[1] / "requirements.txt").read_text(encoding="utf-8")
    assert "\\" not in text
    assert text.endswith("\n")
    assert text.splitlines() == ["ultralytics>=8.3.0", "opencv-python>=4.8.0"]
