from handler import auto_logic
from handler import auto_route
from handler import auto_model
import os
import re
import sys
import logging
from pathlib import Path
from datetime import datetime
from tools.obvious_router import auto_logic

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR
REPORT_LINES = []

DYNAMIC_IMPORT_PATTERNS = [r'\b__import__\b', r'importlib\.import_module', r'importlib\.util', r'\beval\b', r'\bexec\b']
ESSENTIAL_FOLDERS = ["models", "routes", "logic", "tools"]

# @auto_logic
@auto_model
@auto_route
@auto_logic
def log(msg):
    print(msg)
    REPORT_LINES.append(msg)

@auto_model
@auto_route
@auto_logic
def section(title):
    log(f"\n{title}\n{'-' * len(title)}")

@auto_model
@auto_route
@auto_logic
def scan_missing_init_py():
    section("📦 Missing __init__.py files (Package Init Check)")
    missing = []
    for dirpath, dirnames, filenames in os.walk(APP_DIR):
        if "__pycache__" in dirpath or "venv" in dirpath:
            continue
        if "__init__.py" not in filenames:
            log(f" - ❌ {dirpath}")
            missing.append(dirpath)
    if not missing:
        log("✅ All folders have __init__.py")
    return missing

@auto_model
@auto_route
@auto_logic
def scan_dynamic_imports():
    section("🚨 Dynamic Import Suspicion (May cause circular traps)")
    flagged = []
    for dirpath, _, filenames in os.walk(APP_DIR):
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            fullpath = os.path.join(dirpath, fname)
            with open(fullpath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for lineno, line in enumerate(lines, start=1):
                if any(re.search(pattern, line) for pattern in DYNAMIC_IMPORT_PATTERNS):
                    flagged.append((fullpath, lineno, line.strip()))
                    log(f" - ⚠️ {fullpath} [Line {lineno}]: {line.strip()}")
    if not flagged:
        log("✅ No dynamic imports detected.")
    return flagged

@auto_model
@auto_route
@auto_logic
def scan_router_chain():
    section("🔁 Router Chain Detection (include_router check)")
    count = 0
    for dirpath, _, filenames in os.walk(APP_DIR):
        for fname in filenames:
            if fname.endswith(".py"):
                fullpath = os.path.join(dirpath, fname)
                with open(fullpath, "r", encoding="utf-8") as f:
                    if "include_router(" in f.read():
                        log(f" - 🔗 {fullpath}")
                        count += 1
    if count == 0:
        log("✅ No include_router chains found.")
    return count

@auto_model
@auto_route
@auto_logic
def scan_placeholders():
    section("🪫 Placeholder Content (pass, TODO, NotImplemented)")
    flags = ["pass", "# TODO", "raise NotImplementedError", "Dummy", "placeholder"]
    total = 0
    for dirpath, _, filenames in os.walk(APP_DIR):
        for fname in filenames:
            if fname.endswith(".py"):
                with open(os.path.join(dirpath, fname), "r", encoding="utf-8") as f:
                    content = f.read()
                    if any(flag in content for flag in flags):
                        log(f" - ⚠️ {os.path.join(dirpath, fname)}")
                        total += 1
    if total == 0:
        log("✅ No placeholders found.")
    return total

@auto_model
@auto_route
@auto_logic
def check_essential_folders():
    section("📂 Essential Folder Check")
    missing = []
    for folder in ESSENTIAL_FOLDERS:
        full = APP_DIR / folder
        if not full.exists():
            log(f" - ❌ {full}")
            missing.append(folder)
    if not missing:
        log("✅ All essential folders are present.")
    return missing

@auto_model
@auto_route
@auto_logic
def check_pyproject():
    section("📄 pyproject.toml Check")
    if not Path(BASE_DIR / "pyproject.toml").exists():
        log("❌ pyproject.toml not found.")
        return False
    else:
        log("✅ pyproject.toml already exists.")
    return True

@auto_model
@auto_route
@auto_logic
def check_static_folder():
    section("🖼️ Static Folder Check")
    static_dir = APP_DIR / "static"
    if not static_dir.exists():
        log("❌ 'static/' folder missing.")
        return False
    files = list(static_dir.rglob("*.*"))
    if not files:
        log("⚠️ 'static/' exists but is empty.")
        return False
    log(f"✅ 'static/' found with {len(files)} files.")
    return True

@auto_model
@auto_route
@auto_logic
def check_template_routes():
    section("🧩 HTML Template vs Route Check")
    templates_dir = APP_DIR / "templates"
    if not templates_dir.exists():
        log("❌ 'templates/' folder missing.")
        return False
    html_files = list(templates_dir.rglob("*.html"))
    route_names = set()
    for root, _, files in os.walk(APP_DIR / "routes"):
        for f in files:
            if f.endswith(".py"):
                with open(os.path.join(root, f), encoding="utf-8") as file:
                    content = file.read()
                    matches = re.findall(r'@.*\.get\("(/[^"]*)"', content)
                    route_names.update(matches)
    missing_routes = []
    for html in html_files:
        name = html.stem
        if not any(name in r for r in route_names):
            missing_routes.append(html.name)
            log(f"⚠️ No route found for template: {html.name}")
    if not missing_routes:
        log("✅ All templates are mapped to routes.")
    return not missing_routes

@auto_model
@auto_route
@auto_logic
def run_all_checks():
    success = True
    if not check_pyproject(): success = False
    if scan_missing_init_py(): success = False
    if scan_dynamic_imports(): success = False
    if scan_router_chain(): success = False
    if scan_placeholders(): success = False
    if check_essential_folders(): success = False
    return success

if __name__ == "__main__":
    log("\n🔐 SmartSwasthya Prelaunch Checker V3 🔐")
    log("==========================================")

    ready = run_all_checks()

    section("📢 Final Launch Verdict")
    if ready:
        log("🎯 You are absolutely 🎉 ready for 🚀BUILD-UP🚀...!")
    else:
        log("⚠️ Errors found. Please resolve before launch.")

    # Timestamped log saving
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = BASE_DIR / "records" / "prelaunch_logs"
    report_path.mkdir(parents=True, exist_ok=True)
    full_file = report_path / f"prelaunch_report_{ts}.log"
    with open(full_file, "w", encoding="utf-8") as f:
        f.write("\n".join(REPORT_LINES))

    log(f"\n📝 Full Report Saved: {full_file}")
    log("\n💪 Keep pushing! Every fix brings us closer to launch!")