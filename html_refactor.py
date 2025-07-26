import os
import re
import json
from pathlib import Path

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "templates_refactored"
LOG_FILE = "refactor_log.json"
SKIPPED_FILE = "refactor_skipped.json"

# Load class cluster mappings
with open("tailwind_log.json", "r", encoding="utf-8") as f:
    tailwind_data = json.load(f)

# Build reverse utility map
class_to_utility = {}
utility_counter = 1
for file, blocks in tailwind_data.items():
    for block in blocks:
        key = " ".join(sorted(block["classes"]))
        if key not in class_to_utility:
            utility_name = f"utility-{utility_counter}"
            class_to_utility[key] = utility_name
            utility_counter += 1

# Setup logs
refactor_log = {}
refactor_skipped = {}

# Ensure output folder exists
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# Scan and refactor HTML files
for template_file in Path(TEMPLATE_DIR).rglob("*.html"):
    with open(template_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = lines[:]
    template_key = str(template_file.relative_to(TEMPLATE_DIR)).replace("\\", "/")
    template_key = f"{TEMPLATE_DIR}/{template_key}"
    blocks = tailwind_data.get(template_key, [])

    refactor_log[template_key] = []
    refactor_skipped[template_key] = []

    for block in blocks:
        line_num = block["line"]
        original_classes = block["classes"]
        sorted_key = " ".join(sorted(original_classes))
        utility_name = class_to_utility.get(sorted_key)

        if utility_name and line_num < len(updated_lines):
            line = updated_lines[line_num]
            raw_pattern = re.escape(block["raw"])
            regex = re.compile(r'class\s*=\s*"([^"]*?)\b' + raw_pattern + r'\b([^"]*?)"')

            def replacer(match):
                before = match.group(1).strip()
                after = match.group(2).strip()
                combined = " ".join(filter(None, [before, utility_name, after]))
                return f'class="{combined}"'

            updated_line, count = regex.subn(replacer, line)
            if count:
                updated_lines[line_num] = updated_line
                refactor_log[template_key].append({
                    "tag": block.get("tag", "?"),
                    "original": original_classes,
                    "replaced_with": utility_name
                })
            else:
                refactor_skipped[template_key].append({
                    "tag": block.get("tag", "?"),
                    "classes": original_classes
                })
        else:
            refactor_skipped[template_key].append({
                "tag": block.get("tag", "?"),
                "classes": original_classes
            })

    # Write refactored file
    output_path = Path(OUTPUT_DIR) / template_file.name
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

# Save logs
with open(LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(refactor_log, f, indent=2)

with open(SKIPPED_FILE, "w", encoding="utf-8") as f:
    json.dump(refactor_skipped, f, indent=2)

print("🎯 Visual-safe refactor complete.")
print(f"📁 Refactored files: {OUTPUT_DIR}")
print(f"📝 Full log: {LOG_FILE}")
