# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ================================
# 🛠️ UI Integrity Checker
# ================================

import json
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"

UI_JSON = os.path.join(STATIC_DIR, "ui", "ui_module_reference.json")

@auto_model
@auto_route
@auto_logic
def verify_function_in_js(js_file, functions):
    js_path = os.path.join(STATIC_DIR, "js", js_file)
    if not os.path.exists(js_path):
        return False, f"❌ JS file not found: {js_file}"
    with open(js_path, "r", encoding="utf-8") as f:
        js_code = f.read()
        for func in functions:
            if not re.search(r"function\s+" + re.escape(func) + r"\s*\(", js_code):
                return False, f"❌ Function '{func}' not found in {js_file}"
    return True, "✅ All functions exist"

@auto_model
@auto_route
@auto_logic
def run_integrity_check():
    if not os.path.exists(UI_JSON):
        print("❌ ui_module_reference.json not found.")
        return

    with open(UI_JSON, "r", encoding="utf-8") as f:
        module_data = json.load(f)

    for page, ref in module_data.items():
        print(f"\n🔎 Checking: {page}")
        css_path = os.path.join(STATIC_DIR, "css", ref.get("css", ""))
        js_path = os.path.join(STATIC_DIR, "js", ref.get("js", ""))

        if ref.get("css") and not os.path.exists(css_path):
            print(f"❌ Missing CSS: {ref['css']}")
        else:
            print(f"✅ CSS found: {ref.get('css')}")

        if ref.get("js"):
            if os.path.exists(js_path):
                print(f"✅ JS found: {ref['js']}")
                success, message = verify_function_in_js(ref["js"], ref.get("functions", []))
                print(message)
            else:
                print(f"❌ Missing JS: {ref['js']}")

if __name__ == "__main__":
    run_integrity_check()

