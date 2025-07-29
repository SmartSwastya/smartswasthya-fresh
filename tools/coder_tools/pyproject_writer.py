# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# tools/coder_tools/pyproject_writer.py

import os
import logging
from pathlib import Path

# ✅ Dynamically find root/smartswasthya folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PYPROJECT_PATH = BASE_DIR / "pyproject.toml"

DEFAULT_CONTENT = """[project]
name = "smartswasthya"
version = "0.1.0"
description = "Smart Swasthya Seva V3"
authors = ["Smart Dev Team"]
dependencies = [
    "fastapi",
    "uvicorn",
    "jinja2",
    "sqlalchemy",
    "pydantic",
    "python-multipart",
    "aiofiles"
]
requires-python = ">=3.11"

[tool.setuptools]
packages = ["smartswasthya"]

[tool.setuptools.packages.find]
where = ["."]
"""

@auto_model
@auto_route
@auto_logic
def generate_pyproject_if_missing():
    """
    Creates a basic pyproject.toml in the base directory if not already present.
    """
    print(f"📍 Target path to write pyproject.toml: {PYPROJECT_PATH}")  # Debug print

    if PYPROJECT_PATH.exists():
        logging.debug("📄 pyproject.toml already exists.")
        return

    try:
        with open(PYPROJECT_PATH, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CONTENT)
        logging.info(f"🧾 Created default pyproject.toml at {PYPROJECT_PATH}")
    except Exception as e:
        logging.error(f"❌ Failed to create pyproject.toml: {e}")
        print(e)  # Also print exception directly

