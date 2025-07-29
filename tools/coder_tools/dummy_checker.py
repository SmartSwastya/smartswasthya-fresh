# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import os
import re
import logging

DUMMY_PATTERNS = [
    r"lorem ipsum",
    r"dummy\s+data",
    r"\bxyz\b",
    r"\babc\b",
    r"test\s+(text|value|input)",
    r"\bhello world\b",
]

@auto_model
@auto_route
@auto_logic
def log_dummy_outputs():
    """
    Scans all HTML templates for dummy or placeholder content.
    """
    templates_dir = "templates"
    flagged = []

    for dirpath, _, filenames in os.walk(templates_dir):
        for filename in filenames:
            if filename.endswith(".html"):
                path = os.path.join(dirpath, filename)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read().lower()
                except Exception as e:
                    logging.warning(f"⚠️ Failed to read {path}: {e}")
                    continue

                for pattern in DUMMY_PATTERNS:
                    if re.search(pattern, content):
                        flagged.append((path, pattern))
                        break

    if flagged:
        logging.warning("🚫 Dummy or placeholder content found in templates:")
        for path, pattern in flagged:
            logging.warning(f"   └─ {path} (matched: {pattern})")
    else:
        logging.info("✅ No dummy content found in HTML templates.")

