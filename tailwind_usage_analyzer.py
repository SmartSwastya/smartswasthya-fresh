"""
Tailwind Class Usage Analyzer
------------------------------
Scans HTML/Jinja/JS templates for TailwindCSS usage, detects class blocks, logs usage patterns, and suggests potential UI circuits.
"""

import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict
import json

# ---------------------------
# Configurable root folder
# ---------------------------
ROOT_DIR = Path("./templates")  # Can be switched to 'static/', etc.

# ---------------------------
# Patterns to capture class usage
# ---------------------------
CLASS_REGEX = re.compile(r'class\s*=\s*"([^"]+)"')
DYNAMIC_CLASS_REGEX = re.compile(r'class\s*=\s*\{\{([^}]+)\}\}')
JS_CLASS_REGEX = re.compile(r'(?:classList\\.add\(|className\s*=\s*)(["\'])(.*?)\1')

# ---------------------------
# UI Circuit Heuristics
# ---------------------------
UI_PATTERNS = {
    "grid-layout": ["grid", "grid-cols-", "gap-"],
    "card-block": ["bg-", "rounded-", "shadow-"],
    "button-block": ["btn", "px-", "py-", "text-", "hover:"],
    "alert-block": ["bg-red-", "bg-yellow-", "bg-green-", "text-white"],
    "nav-flex": ["flex", "items-center", "justify-"]
}

# ---------------------------
# Main Analysis Engine
# ---------------------------
def extract_classes_from_line(line):
    matches = CLASS_REGEX.findall(line)
    dynamic = DYNAMIC_CLASS_REGEX.findall(line)
    js_matches = JS_CLASS_REGEX.findall(line)
    return matches + dynamic + [j[1] for j in js_matches]

def detect_ui_pattern(classlist):
    found = []
    for name, triggers in UI_PATTERNS.items():
        if any(any(cls.startswith(t) for cls in classlist) for t in triggers):
            found.append(name)
    return found

def scan_file(filepath):
    results = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f.readlines(), 1):
            class_groups = extract_classes_from_line(line)
            for class_str in class_groups:
                classes = class_str.split()
                pattern_tags = detect_ui_pattern(classes)
                results.append({
                    'line': i,
                    'classes': classes,
                    'patterns': pattern_tags,
                    'raw': class_str.strip()
                })
    return results

def recursive_scan(root):
    log = defaultdict(list)
    for path in root.rglob("*.html"):
        res = scan_file(path)
        if res:
            log[str(path)] = res
    return log

# ---------------------------
# Output Formatting
# ---------------------------
def pretty_print(log):
    for file, blocks in log.items():
        print(f"\n📄 {file}")
        for block in blocks:
            line = block['line']
            clz = ', '.join(block['classes'])
            tags = ', '.join(block['patterns'])
            print(f"  L{line:03}: {clz}  --> [{tags}]")

def write_json(log, out_path="tailwind_log.json"):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2)

# ---------------------------
# Entrypoint
# ---------------------------
if __name__ == "__main__":
    root = ROOT_DIR if len(sys.argv) < 2 else Path(sys.argv[1])
    result = recursive_scan(root)
    pretty_print(result)
    write_json(result)
    print("\n✅ Tailwind usage analysis completed. Output saved to tailwind_log.json")
