# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
#!/usr/bin/env python3

import sys
import os
from logging.config import fileConfig
from alembic import command
from alembic.config import Config

# Ensure local package path
from pathlib import Path
PROJECT_ROOT = str(Path(__file__).resolve().parent / "smartswasthya")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@auto_model
@auto_route
@auto_logic
def run_migrations():
    try:
        config = Config("alembic.ini")  # this stays same IF file is in root/smartswasthya/
        if os.path.exists("alembic.ini"):
            fileConfig(config.config_file_name)
        print("🚀 Running Alembic upgrade to head...")
        command.upgrade(config, "head")
        print("✅ Alembic upgrade complete.")
    except Exception as e:
        print(f"❌ Alembic migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()


