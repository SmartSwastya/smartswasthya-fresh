# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
import os
import json
import re
import traceback
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # root/smartswasthya
OUTPUT_FILE = BASE_DIR / "records" / "indentation_error_map.json"
TARGET_EXTENSIONS = [".py", ".html"]

error_map = []

# ----------------------------------------
# @auto_flag: exec_eval_compile [compile]
# ⚠️ Avoid eval/exec unless sandboxed
# @auto_flag: exec_eval_compile [compile]
# ⚠️ Avoid eval/exec unless sandboxed
# @auto_flag: exec_eval_compile [compile]
# ⚠️ Avoid eval/exec unless sandboxed
# 🔍 Scan Python files (via compile)
# ----------------------------------------
def scan_python(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        compile(source, file_path.name, 'exec')  # Triggers syntax/indentation errors
    except (IndentationError, SyntaxError) as e:
        return {
            "file": str(file_path.relative_to(BASE_DIR)).replace("\\", "/"),
            "line": getattr(e, "lineno", "?"),
            "error": str(e)
        }
    return None

# ----------------------------------------
# 🔍 Scan HTML files (basic Jinja & tag balance)
# ----------------------------------------
def scan_html(file_path):
    errors = []
    jinja_stack = []
    div_stack = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):
        l = line.strip()

        # Check tab/space mix
        if "\t" in line and "    " in line:
            errors.append({
                "line": i,
                "error": "Mixed tabs and spaces"
            })

        # Check Jinja blocks
        if "{% if" in l or "{% for" in l or "{% block" in l:
            jinja_stack.append((l, i))
        if "{% endif" in l or "{% endfor" in l or "{% endblock" in l:
            if jinja_stack:
                jinja_stack.pop()
            else:
                errors.append({
                    "line": i,
                    "error": "Unmatched Jinja end tag"
                })

        # Check <div> balancing
        if "<div" in l:
            div_stack.append(i)
        if "</div>" in l:
            if div_stack:
                div_stack.pop()
            else:
                errors.append({
                    "line": i,
                    "error": "Unmatched </div>"
                })

    # Any unmatched opening tags left
    for _, i in jinja_stack:
        errors.append({
            "line": i,
            "error": "Unclosed Jinja block"
        })
    for i in div_stack:
        errors.append({
            "line": i,
            "error": "Unclosed <div>"
        })

    if errors:
        return {
            "file": str(file_path.relative_to(BASE_DIR)).replace("\\", "/"),
            "errors": errors
        }
    return None

# ----------------------------------------
# 📦 Unified scan wrapper
# ----------------------------------------
def scan_file(file_path):
    if file_path.suffix == ".py":
        result = scan_python(file_path)
        if result:
            error_map.append(result)
    elif file_path.suffix == ".html":
        result = scan_html(file_path)
        if result:
            error_map.append(result)

# ----------------------------------------
# 🚀 Run full project scan
# ----------------------------------------
def run_scan():
    for root, _, files in os.walk(BASE_DIR):
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix in TARGET_EXTENSIONS and "__pycache__" not in str(fpath):
                scan_file(fpath)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(error_map, f, indent=2)

    print(f"✅ Scan complete. {len(error_map)} file(s) with error(s).")
    print(f"📄 Output → {OUTPUT_FILE}")

if __name__ == "__main__":
    run_scan()
