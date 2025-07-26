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
import json
from pathlib import Path

from tools.file_utils import save_json

ROOT_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT_DIR / "templates"
OUTPUT_FILE = ROOT_DIR / "template_trace.json"

# Regex patterns for Jinja and Starlette/FastAPI template usage
TEMPLATE_PATTERNS = [
    r'render_template\s*\(\s*["\']([^"\']+\.html)["\']',
    r'TemplateResponse\s*\(\s*["\']([^"\']+\.html)["\']',
]

@auto_model
@auto_route
@auto_logic
def find_all_templates():
    return sorted([
        str(p.relative_to(TEMPLATES_DIR)).replace("\\", "/")
        for p in TEMPLATES_DIR.rglob("*.html")
    ])

@auto_model
@auto_route
@auto_logic
def find_templates_in_code(py_path):
    with open(py_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = []
    for pattern in TEMPLATE_PATTERNS:
        matches += re.findall(pattern, content)
    return list(set(matches))  # remove duplicates

@auto_model
@auto_route
@auto_logic
def generate_template_trace():
    trace_map = {}  # template → list of source files

    all_py_files = list(ROOT_DIR.rglob("*.py"))
    for py_file in all_py_files:
        rel_path = str(py_file.relative_to(ROOT_DIR)).replace("\\", "/")
        matched_templates = find_templates_in_code(py_file)
        for template in matched_templates:
            trace_map.setdefault(template.strip(), []).append(rel_path)

    all_templates = find_all_templates()

    flat_result = []
    for template in all_templates:
        source_files = trace_map.get(template, [])
        flat_result.append({
            "template": template,
            "source_files": sorted(set(source_files)),
        })

    save_json(flat_result, OUTPUT_FILE)
    print(f"OK: template_trace.json saved.")
    print(f"Good Templates found: {len(flat_result)}")
    return flat_result


if __name__ == "__main__":
    generate_template_trace()
