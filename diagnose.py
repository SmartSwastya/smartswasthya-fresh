# ░█▀█░█▀█░█▀█░█▀▄░▀█▀░█▀█░█▀▄░█▀▀
# ░█▀▀░█░█░█░█░█▀▄░░█░░█░█░█▀▄░▀▀█
# ░▀░░░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀

# 📦 diagnose.py — Smart Trace Fallback Tool
# 🔍 Usage: trace_keyword("tools") → list of code lines with match

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import os

EXCLUDE_DIRS = {"__pycache__", ".git", ".idea", ".vscode", "records", "static", "templates", "node_modules"}
VALID_FILES = {".py", ".env", "Dockerfile", "Makefile"}

def is_valid_file(filename):
    return (
        filename.endswith(tuple(VALID_FILES)) or
        filename in VALID_FILES
    )

def trace_keyword(keyword):
    matches = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if is_valid_file(file):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f):
                            if keyword in line:
                                matches.append(f"{path}:{i + 1}: {line.strip()}")
                except Exception:
                    continue
    return matches or [f"❌ No trace found for '{keyword}'"]
