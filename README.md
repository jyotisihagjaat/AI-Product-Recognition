# AI Product Recognition V2

Original project by [jyotisihagjaat](https://github.com/jyotisihagjaat). This version builds on that work with the fixes described in [What changed in this update](#what-changed-in-this-update).

This version learns your own 13 physical products from webcam photos. The previous YOLO-World version tried generic text-based detection, which can be slow and unreliable for specific products.

## Important
For accurate recognition of your exact items, collect example photos first. Aim for 30-50 varied photos per product (different angles, distances, and backgrounds). Training is a one-time step and can take several minutes on CPU. Training and live recognition both use a small classifier at 160px on the same centred square crop. Speed depends on your laptop.

## Setup (VS Code PowerShell)
Double-click `setup.bat`. It creates `.venv` and installs `requirements.txt`. If you already have a `.venv`, you can instead run:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run order
`setup.bat` -> `src\collect_data.py` -> `src\train_model.py` -> `run.bat`

## What changed in this update
The original project already had the right idea: learn your own products from webcam photos instead of relying on generic text prompts. This update keeps that design, the same tools and the same training recipe, and fixes the things that stopped it working reliably.

| Change | Before | Now | Why it is better |
|---|---|---|---|
| Install | `requirements.txt` was one line with literal `\n` characters, so `pip install -r` failed | Two proper lines | `setup.bat` installs cleanly on a fresh machine |
| Launcher | `run.bat` started the old YOLO-World version | `run.bat` starts V2 recognition | Double-clicking runs the app the README describes |
| What the model sees | Trained on a centred square at 160px, but recognised the full frame at 224px | Recognition uses the same centred square at 160px, shown as a green box | The model is shown the same kind of image it learned from, with no retraining needed |
| Unsure predictions | Always showed the top guess, even at low confidence | Shows "Unknown" below a threshold (60% by default) | Fewer confident-looking wrong answers |
| Labels | Showed folder names like `body_lotion` | Shows display names like `Body Lotion` | Easier to read |
| Missing model or camera | Crashed with a Python traceback | Prints what to do and exits cleanly | Clear next steps instead of an error dump |
| Lost camera feed | Retried in a tight loop forever | Pauses between retries and stops after about 1.5 seconds | No frozen window or maxed-out CPU |
| Saving photos | Deleting a photo could make the next save overwrite an existing one | New photos always get the next free number | Collected photos are never lost |
| Training with too few photos | Deleted `dataset/` first, then stopped at the first short product | Checks every product first and lists all the short ones | Nothing is deleted when training cannot start, and you see every product to fix at once |
| Class list | Defined twice (V1 and V2) | One list in `src/labels.py` | Products cannot drift out of sync |
| Settings | Scattered through several files | In `src/config.py` | One place to change the camera, threshold or crop |
| Tests | None | `pytest` tests for the helpers and labels | Changes can be checked without a camera |

The 60% threshold is a starting point, not a measured value. If good predictions show as "Unknown", lower `CONF_THRESHOLD` in `src/config.py`; if wrong guesses get through, raise it.

## 1. Collect photos
```powershell
.\.venv\Scripts\python.exe src\collect_data.py
```
Press the product letter shown on screen to select it, then SPACE to save a photo. Press Q to quit. Repeat until each product has 30-50 varied photos.

## 2. Train once
```powershell
.\.venv\Scripts\python.exe src\train_model.py
```
Every product needs at least 10 photos. If any are short, training lists them all and stops without touching `dataset/`.

## 3. Run live recognition
Double-click `run.bat`, or:
```powershell
.\.venv\Scripts\python.exe src\recognize.py
```
Show one product at a time inside the green square; only that square is classified, just like the collected photos. If the top confidence is below `CONF_THRESHOLD` (60% by default) the label shows "Unknown". Press Q to quit. If no model has been trained yet, the app tells you which commands to run.

## Settings
`src/config.py` holds `CAMERA_INDEX` (try 1 if the wrong camera opens), `CONF_THRESHOLD`, and the crop and image size, which must match between collection, training and recognition.

## Tips
Use bright light, keep the item centred and reasonably large, and capture different angles/backgrounds. If two products are confused, collect more varied examples of those two and retrain. Confidence is an estimate, not a guarantee.

## Legacy V1
`src/product_detector.py` is the older YOLO-World version. It is kept for reference and reads its classes from `src/labels.py`; `run.bat` starts V2.

## Tests
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
```
The tests cover the pure helpers and labels; they need no camera or model.

## GitHub
`.gitignore` excludes raw photos, datasets, model weights, and virtual environments. Upload the code and README; avoid uploading private photos.
