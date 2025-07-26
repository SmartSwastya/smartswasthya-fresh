# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import subprocess
import time
import os
import hashlib
import threading
from pathlib import Path

WATCH_DIR = Path(".")  # Root directory
PS1_SCRIPT = "smart_docker.ps1"
CHECK_INTERVAL = 3  # seconds
EXTENSIONS = [".py", ".html", ".json", ".js", ".ts", ".css", ".env", ".yml", ".toml"]

last_hashes = {}

@auto_model
@auto_route
@auto_logic
def hash_file(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

@auto_model
@auto_route
@auto_logic
def scan_changes():
    changed = False
    current = {}
    for root, _, files in os.walk(WATCH_DIR):
        if any(skip in root for skip in ["__pycache__", ".git", ".idea", ".vscode", "node_modules"]):
            continue
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                path = os.path.join(root, file)
                current[path] = hash_file(path)

    # Detect changes
    for path, hashval in current.items():
        if path not in last_hashes or last_hashes[path] != hashval:
            print(f"🔄 Change detected in: {path}")
            changed = True
    last_hashes.clear()
    last_hashes.update(current)
    return changed

@auto_model
@auto_route
@auto_logic
def run_ps1():
    print("\n🚀 Running Docker build via smart_docker.ps1 ...")
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", PS1_SCRIPT], check=True)
        print("✅ Build step successful.")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Build error occurred. Waiting for changes to resume...")
        return False

@auto_model
@auto_route
@auto_logic
def monitor_loop():
    print("🧠 Smart Build Simulator Started. Press Ctrl+C to exit.")
    success = run_ps1()

    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            if scan_changes():
                print("🔁 Retrying build after file changes...")
                success = run_ps1()
        except KeyboardInterrupt:
            print("\n🛑 Manual exit. Simulator stopped.")
            break

if __name__ == "__main__":
    monitor_loop()
