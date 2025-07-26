# ░█▀█░█▀█░█▀█░█▀▄░▀█▀░█▀█░█▀▄░█▀▀
# ░█▀▀░█░█░█░█░█▀▄░░█░░█░█░█▀▄░▀▀█
# ░▀░░░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀
#
# ⚕️ Corrupted File Restore Plan
# 📌 Target: Remove looped marker injections, fix redundant imports
# 🧠 Based on Smart Trace Analysis
# 🔐 Source: root_161.tar (POST smart_correction.py corruption)
# ———————————————————————————————

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

CORRUPTED_TARGETS = [
    "odil/generate_model_trace.py",
    "registry/logic_autodiscover.py",
    "routes/misc/dev_auth_routes.py",
    "tools/devops/inspector.py",
    "tools/coder_tools/patcher.py",
    "tools/devops/detect_suspicious_code.py",
]

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    seen_imports = set()
    for line in lines:
        # Remove duplicate obvious_router import
        if 'from tools.obvious_router import' in line:
            if 'obvious_router' in seen_imports:
                continue
            seen_imports.add('obvious_router')
        # Deduplicate @auto_* or @trace markers
        if re.search(r'#\s*@(?:auto_|trace)', line):
            if line.strip() in cleaned_lines:
                continue
        cleaned_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

    print(f"🧽 Cleaned: {file_path}")

if __name__ == "__main__":
    print("🔧 Smart Restore Started...\n")
    for rel_path in CORRUPTED_TARGETS:
        abs_path = os.path.join(ROOT, rel_path)
        if os.path.exists(abs_path):
            clean_file(abs_path)
        else:
            print(f"⚠️ Not found: {rel_path}")
    print("\n✅ Restore Complete.")
