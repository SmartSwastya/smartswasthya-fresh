"""
Tailwind Optimizer Utility
---------------------------
Processes tailwind_log.json and:
1. Extracts reusable class blocks
2. Writes safelist to tailwind.config.js
3. Writes @apply blocks to input.utilities.css

Usage:
  python tailwind_optimizer.py --min-reuse 4
"""

import json
import argparse
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------
# CLI Argument Parsing
# ---------------------------
parser = argparse.ArgumentParser(description="Tailwind Optimizer")
parser.add_argument("--min-reuse", type=int, default=4, help="Minimum reuse count for a utility block")
parser.add_argument("--config", type=str, default="tailwind.config.js", help="Path to Tailwind config")
parser.add_argument("--output", type=str, default="static/css/input.utilities.css", help="Output CSS file for utilities")
parser.add_argument("--logfile", type=str, help="Optional logfile to write extracted log")
args = parser.parse_args()

# ---------------------------
# Load Log
# ---------------------------
with open("tailwind_log.json", "r", encoding="utf-8") as f:
    data = json.load(f)

class_counter = Counter()
block_patterns = defaultdict(list)

for file, entries in data.items():
    for entry in entries:
        classes = tuple(sorted(entry['classes']))
        class_counter.update(classes)
        key = ", ".join(classes)
        block_patterns[key].append((file, entry['line']))

# ---------------------------
# Generate Safelist
# ---------------------------
safelist = sorted(set(cls for cls, count in class_counter.items() if count >= 3))

config_path = Path(args.config)
config_lines = []
if config_path.exists():
    with open(config_path, "r", encoding="utf-8") as f:
        config_lines = f.readlines()

with open(config_path, "w", encoding="utf-8") as f:
    inside_config = False
    for line in config_lines:
        if 'safelist' in line:
            continue  # remove previous safelist
        if 'module.exports' in line:
            inside_config = True
        f.write(line)
        if inside_config and '{' in line:
            f.write("  safelist: [\n")
            for cls in safelist:
                f.write(f"    '{cls}',\n")
            f.write("  ],\n")
            inside_config = False

print(f"✅ Safelist written to: {args.config}")

# ---------------------------
# Generate Utilities
# ---------------------------
common_blocks = {k: v for k, v in block_patterns.items() if len(v) >= args.min_reuse}
output_path = Path(args.output)
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write("/* Auto-generated reusable utility classes */\n\n")
    for i, (block, locations) in enumerate(common_blocks.items(), 1):
        classname = f".utility-{i}"
        f.write(f"{classname} {{\n  @apply {block};\n}}\n\n")

print(f"✅ Reusable utilities written to: {args.output}")

# ---------------------------
# Optional Log
# ---------------------------
if args.logfile:
    with open(args.logfile, "w", encoding="utf-8") as logf:
        json.dump({k: v for k, v in common_blocks.items()}, logf, indent=2)
    print(f"📝 Log written to: {args.logfile}")
