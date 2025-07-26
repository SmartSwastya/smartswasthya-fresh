# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# tools/file_utils.py
import re
import json
import unicodedata
from pathlib import Path
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# 📁 tools/file_utils.py

@auto_model
@auto_route
@auto_logic
def write_json(data, path, indent=2):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)

@auto_model
@auto_route
@auto_logic
def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@auto_model
@auto_route
@auto_logic
def save_json(data, path):
    """
    Saves JSON data to the given file path.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def secure_filename(filename):
    """
    Sanitize filename to be safe for use in filesystem.
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")
    filename = re.sub(r"[^\w.-]", "_", filename)
    return filename.strip("._")
