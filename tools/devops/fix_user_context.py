# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import os
import re

TARGET_FILES = [
    "routes/admin_login_routes.py",
    "routes/base_routes.py",
    "routes/console_dashboard_routes.py",
    "routes/dev_auth_routes.py",
    "routes/dev_bucket_routes.py",
    "routes/dev_login_routes.py",
    "routes/landing_routes.py",
    "routes/login_routes.py",
    "routes/rollback_viewer_routes.py",
    "routes/scan_results_routes.py",
    "routes/signup_routes.py",
    "routes/smartuser_dashboard_routes.py",
    "routes/submission_result_routes.py",
    "routes/sync_results_routes.py",
    "routes/dev/console_dashboard_routes.py",
    "routes/dev/scan_results_routes.py",
    "routes/dev/sync_results_routes.py",
    "routes/dev/ui_dev_reference_viewer_routes.py",
]

@auto_model
@auto_route
@auto_logic
def patch_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if 'TemplateResponse(' in line and '{"request": request' in line and 'user' not in line:
            if "smartuser" in file_path or "profile" in file_path or "dashboard" in file_path:
                inject = '"current_user": user'
            else:
                inject = '"user": user'

            line = line.replace('{"request": request', f'{{"request": request, {inject}')
        new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"✅ Patched: {file_path}")

if __name__ == "__main__":
    for file in TARGET_FILES:
        if os.path.exists(file):
            patch_file(file)
        else:
            print(f"⚠️ Skipped (not found): {file}")

