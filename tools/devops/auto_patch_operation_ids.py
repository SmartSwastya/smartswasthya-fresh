# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
from pathlib import Path
import os
from tools.smart_logger import SmartLogger
import re

logger = SmartLogger("AutoPatcher")

TARGET_FOLDERS = [
    Path(__file__).resolve().parent.parent.parent / "app" / "routes",
    Path(__file__).resolve().parent.parent.parent / "app" / "blueprints",
]

@auto_model
@auto_route
@auto_logic
def patch_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'@(router\w*)\.(get|post|put|delete|patch)\("([^"]+)"(?:, *.*)?\)'
    matches = re.findall(pattern, content)

    if not matches:
        return False

    patched = False
    for router_var, method, route in matches:
        operation_id = f"{method}_{route.strip('/').replace('/', '_')}"
        if f'operation_id="{operation_id}"' not in content:
            escaped_router = re.escape(router_var)
            escaped_route = re.escape(route)
            pattern_to_replace = rf'@{escaped_router}\.{method}\("{escaped_route}"'
            content = re.sub(
                pattern_to_replace,
                f'@{router_var}.{method}("{route}", operation_id="{operation_id}"',
                content
            )
            patched = True

    if patched:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.log_success("Patched", file_path.name, f"✅ Patched: {file_path}")
    else:
        logger.log_info("Skipped", file_path.name, f"⏭️ Already OK")

    return patched

@auto_model
@auto_route
@auto_logic
def run_patch():
    target_dirs = ["routes", "blueprints"]
    for target_dir in target_dirs:
        logger.log_info("Scanning", "AutoPatcher", f"🔍 Scanning for FastAPI routes in: {target_dir}")
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = Path(root) / file
                    patch_file(file_path)

if __name__ == "__main__":
    run_patch()

