# The only class list. (key, display name, folder, YOLO-World prompt for legacy V1)
PRODUCTS = [
    ("a", "Phone", "phone", "smartphone"),
    ("b", "Charger", "charger", "phone charger"),
    ("c", "Bangle", "bangle", "bangle bracelet"),
    ("d", "Body Lotion", "body_lotion", "body lotion bottle"),
    ("e", "Lipgloss", "lipgloss", "lip gloss tube"),
    ("f", "Spoon", "spoon", "spoon"),
    ("g", "Bournvita", "bournvita", "Bournvita drink container"),
    ("h", "Snacks", "snacks", "packaged snack packet"),
    ("i", "Notebook", "notebook", "notebook"),
    ("j", "Pen", "pen", "pen"),
    ("k", "Glue", "glue", "glue bottle"),
    ("l", "Cup", "cup", "drinking cup"),
    ("m", "Bottle", "bottle", "water bottle"),
]

DISPLAY_NAMES = {folder: name for _, name, folder, _ in PRODUCTS}
PROMPTS = [prompt for *_, prompt in PRODUCTS]
