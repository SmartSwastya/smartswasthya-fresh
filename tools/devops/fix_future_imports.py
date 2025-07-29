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

@auto_model
@auto_route
@auto_logic
def fix_future_line(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    future_line_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "from __future__ import annotations":
            future_line_idx = i
            break

    if future_line_idx is not None and future_line_idx > 0:
        # Remove it and insert at the top
        line = lines.pop(future_line_idx)
        lines.insert(0, line)
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return True
    return False


patched = []
for root, dirs, files in os.walk("models"):
    for file in files:
        if file.endswith(".py"):
            fpath = os.path.join(root, file)
            if fix_future_line(fpath):
                patched.append(fpath)

print(f"✅ Future import repositioned in {len(patched)} files")
for p in patched:
    print("✔️", p)

