# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# tools/devops/fix_timestamp_imports.py
import os

@auto_model
@auto_route
@auto_logic
def fix_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated = False

    # Ensure import for Column and DateTime
    has_sa_import = False
    for i, line in enumerate(lines):
        if "from sqlalchemy import" in line:
            if "Column" in line and "DateTime" not in line:
                lines[i] = line.strip().rstrip() + ", DateTime\n"
                updated = True
            if "Column" not in line and "DateTime" not in line:
                lines[i] = line.strip().rstrip() + " Column, DateTime\n"
                updated = True
            has_sa_import = True

    if not has_sa_import:
        lines.insert(0, "from sqlalchemy import Column, DateTime\n")
        updated = True

    # Ensure func import
    if not any("from sqlalchemy.sql import func" in l for l in lines):
        lines.insert(1, "from sqlalchemy.sql import func\n")
        updated = True

    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return True
    return False


patched = []
for root, dirs, files in os.walk("models"):
    for fname in files:
        if fname.endswith(".py"):
            fpath = os.path.join(root, fname)
            if fix_imports(fpath):
                patched.append(fpath)

print(f"✅ Patched files: {len(patched)}")
for p in patched:
    print("✔️", p)

