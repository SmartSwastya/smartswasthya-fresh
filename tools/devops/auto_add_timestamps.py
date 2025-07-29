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
from pathlib import Path
import re

MODELS_DIR = Path("models")  # relative to project root

created_at_line = "    created_at = Column(DateTime(timezone=True), server_default=func.now())"
updated_at_line = "    updated_at = Column(DateTime(timezone=True), onupdate=func.now())"

@auto_model
@auto_route
@auto_logic
def has_timestamps(content):
    return "created_at" in content and "updated_at" in content

@auto_model
@auto_route
@auto_logic
def patch_model_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    content = "".join(lines)
    if has_timestamps(content):
        return False  # already patched

    patched = False
    for i, line in enumerate(lines):
        if line.strip().startswith("class ") and "(Base)" in line:
            indent = re.match(r"\s*", line).group(0)
            insert_at = i + 1
            # find end of class decorators if any
            while insert_at < len(lines) and lines[insert_at].strip().startswith("@"):
                insert_at += 1
            lines.insert(insert_at + 1, f"{indent}{created_at_line}\n")
            lines.insert(insert_at + 2, f"{indent}{updated_at_line}\n")
            patched = True
            break

    if patched:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    return patched

@auto_model
@auto_route
@auto_logic
def main():
    patched_files = []
    for file in MODELS_DIR.rglob("*.py"):
        if patch_model_file(file):
            patched_files.append(file)

    print(f"🎯 Total patched files: {len(patched_files)}")
    for f in patched_files:
        print(f"✅ {f}")

if __name__ == "__main__":
    main()

