# Add at top: import sys; sys.stdout.reconfigure(encoding='utf-8')

updated_auto_migrate = """
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# ─────────────────────────────────────────────────────────────
# ✅ AUTO MIGRATION SCRIPT (Safe + Smart)
# Location: root/smartswasthya/tools/devops/auto_migrate.py
# ─────────────────────────────────────────────────────────────

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Encoding fix for Windows
import time
import socket
import subprocess
from pathlib import Path

# Set up project root for dynamic imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Smart markers (if used for tracking)
from handler import auto_model, auto_route, auto_logic
from alembic_runner import run_migrations  # optional if used in future

@auto_model
@auto_route
@auto_logic
def wait_for_db(host="localhost", port=5432, retries=20, delay=3):  # Change to localhost
    for attempt in range(1, retries + 1):
        try:
            with socket.create_connection((host, port), timeout=2):
                print("Database is reachable.")
                return
        except (ConnectionRefusedError, OSError):
            print(f"Waiting for DB at {host}:{port}... (attempt {attempt}/{retries})")
        time.sleep(delay)
    print("Database not reachable after multiple attempts.")
    sys.exit(1)

@auto_model
@auto_route
@auto_logic
def run_cmd(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(result.stderr.strip())
        sys.exit(1)
    print(result.stdout.strip())

@auto_model
@auto_route
@auto_logic
def main():
    print("Checking if migration is needed...")

    # Make sure DB is reachable before migration
    wait_for_db()

    # Step 1: Run upgrade always (safe if already up-to-date)
    run_cmd("alembic upgrade head")

    print("Migration successful.")

if __name__ == "__main__":
    main()
"""

# Apply: auto_migrate.py मध्ये हे paste कर.