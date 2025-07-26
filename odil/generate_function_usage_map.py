# ╔════════════════════════════════════════════════╗
# ║ generate_function_usage_map.py (Refactored)   ║
# ╚════════════════════════════════════════════════╝

import os, re, json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "function_usage_map.json"
EXCLUDE_DIRS = {"__pycache__", ".git", ".idea", ".vscode", "node_modules", "records", "static"}

def get_py_files(base):
    py_files = []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(".py"):
                py_files.append(Path(root) / file)
    print("📁 Python files found:", len(py_files))
    return py_files

def extract_defined_functions(file_path):
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        return re.findall(r"^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", content, flags=re.MULTILINE)
    except Exception:
        return []

def extract_all_definitions(py_files):
    func_map = {}
    for path in py_files:
        defined = extract_defined_functions(path)
        for fn in defined:
            func_map[fn] = str(path.relative_to(PROJECT_ROOT))
    print("🧠 Total functions detected:", len(func_map))
    return func_map

def find_usages(py_files, func_defs):
    usage_map = {fn: [] for fn in func_defs}
    for path in py_files:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for fn in func_defs:
            if func_defs[fn] == str(path.relative_to(PROJECT_ROOT)):
                continue  # Skip self-usage
            if re.search(rf"(?<!def\s){re.escape(fn)}\s*\(", content):
                usage_map[fn].append(str(path.relative_to(PROJECT_ROOT)))
    return usage_map

# ✅ Exportable wrapper for external import
def generate_function_usage_map():
    return generate_usage_map()

# 🧩 Internal main function
def generate_usage_map():
    print("🔍 PROJECT_ROOT =", PROJECT_ROOT)
    py_files = get_py_files(PROJECT_ROOT)
    func_defs = extract_all_definitions(py_files)
    usage_map = find_usages(py_files, func_defs)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(usage_map, f, indent=2)
    print(f"✅ function_usage_map.json saved at: {OUTPUT_PATH}")
    return usage_map

# ▶️ CLI Entry
if __name__ == "__main__":
    generate_function_usage_map()
