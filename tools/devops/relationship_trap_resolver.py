# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import re
from pathlib import Path
from shutil import copy2

# ✅ STEP 1: Resolve project root containing models/ and main.py
for parent in Path(__file__).resolve().parents:
    if (parent / "models").exists() and (parent / "main.py").exists():
        BASE_DIR = parent
        break
else:
    raise RuntimeError("❌ Could not locate smartswasthya project directory.")

MODEL_DIR = BASE_DIR / "models"
BACKUP_SUFFIX = ".bak"
patch_log = []

print(f"📁 Resolved MODEL_DIR = {MODEL_DIR}")

# ✅ STEP 2: Patch __init__.py → Lazy loader
init_file = MODEL_DIR / "__init__.py"
if init_file.exists():
    copy2(init_file, str(init_file) + BACKUP_SUFFIX)
    content = init_file.read_text(encoding="utf-8")
    model_names = re.findall(r"from \.([a-zA-Z0-9_\.]+) import", content)

    lazy_loader_code = f"""# 🚨 Lazy Model Import to prevent circular references
import importlib
model_list = {sorted(set(model_names))}
for model_name in model_list:
# @auto_flag: dynamic_imports [importlib.import_module]
# ⚠️ Dynamic import detected — avoid in core logic
# @auto_flag: dynamic_imports [importlib.import_module]
# ⚠️ Dynamic import detected — avoid in core logic
# @auto_flag: dynamic_imports [importlib.import_module]
# ⚠️ Dynamic import detected — avoid in core logic
    importlib.import_module(f"models.{{model_name}}")
"""
    patched = re.sub(r"(from \.[a-zA-Z0-9_\.]+ import .+)+", lazy_loader_code, content, flags=re.MULTILINE)
    init_file.write_text(patched, encoding="utf-8")
    patch_log.append(f"Patched: models/__init__.py → lazy load of {len(model_names)} modules.")

# ✅ STEP 3: Patch model files safely
for pyfile in MODEL_DIR.rglob("*.py"):
    content = pyfile.read_text(encoding="utf-8")
    original = content
    updated = content

    copy2(pyfile, str(pyfile) + BACKUP_SUFFIX)

    # (A) relationship("models.users.User") → relationship("User")
    updated = re.sub(r'relationship\(["\']models\.users\.User["\']', 'relationship("User"', updated)

    # (B) Remove unused `from models.users import User`
    if 'from models.users import User' in updated:
        if re.search(r'relationship\("User"', updated) and not re.search(r'class\s+User\(', updated):
            updated = re.sub(r'from models\.users import User\s*\n?', '', updated)

    # (C) Ensure TYPE_CHECKING block contains only `import` statements
    updated = re.sub(
        r'(?s)(if TYPE_CHECKING:\n)([ \t]+.*\n)+',
        'if TYPE_CHECKING:\n    from models.users import User\n',
        updated
    )

    # Never touch `class` indentation or definition location

    if updated != original:
        pyfile.write_text(updated, encoding="utf-8")
        patch_log.append(f"Patched: {pyfile.relative_to(BASE_DIR)}")

# ✅ Final log
print("\n🛠️ Smart Relationship Trap Resolver v4 Completed.\n")
if patch_log:
    print("✅ Patch Summary:")
    print("\n".join(patch_log))
else:
    print("ℹ️ No changes were necessary — everything already clean.")
