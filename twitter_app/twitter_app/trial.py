import os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

template = os.path.join(BASE_DIR, "templates")
print(template)
print("*******************")