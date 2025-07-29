from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ╔════════════════════════════════════════════════════════════════════╗
# ║         SMART SWASTHYA – FILE SCANNER UTILITIES MODULE            ║
# ║    Shared by checker_tool, scan, sync, handler for core logic    ║
# ╚════════════════════════════════════════════════════════════════════╝

import os
import tarfile
import datetime

# ⛔ Paths to exclude
SKIP_DIRS = {'.git', '__pycache__', '.bak', '.venv', '.idea', '.mypy_cache'}
SKIP_FILES = {'app.py', 'main.py', 'Dockerfile', 'docker-compose.yml'}

# ════════════════════════════════════════
# 🔍 Should skip logic
# ════════════════════════════════════════
@auto_model
@auto_route
@auto_logic
def should_skip_path(path: str) -> bool:
    parts = path.split(os.sep)
    return any(p in SKIP_DIRS for p in parts) or os.path.basename(path) in SKIP_FILES

# ════════════════════════════════════════
# 📁 List All Valid Files
# ════════════════════════════════════════
@auto_model
@auto_route
@auto_logic
def list_all_files(base_dir: str, extension: str = ".py") -> list:
    valid_files = []
    for dirpath, _, filenames in os.walk(base_dir):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if full_path.endswith(extension) and not should_skip_path(full_path):
                valid_files.append(full_path)
    return valid_files

# ════════════════════════════════════════
# 🕒 Filter by Modified Time
# ════════════════════════════════════════
@auto_model
@auto_route
@auto_logic
def filter_files_by_time(base_dir: str, start_time: datetime.datetime, end_time: datetime.datetime) -> list:
    filtered = []
    for dirpath, _, filenames in os.walk(base_dir):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if should_skip_path(full_path): continue
            try:
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
                if start_time <= mtime <= end_time:
                    filtered.append(full_path)
            except Exception:
                continue
    return filtered

# ════════════════════════════════════════
# 📦 Tar Extractor
# ════════════════════════════════════════
@auto_model
@auto_route
@auto_logic
def extract_tar_file(tar_path: str, target_dir: str):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    with tarfile.open(tar_path) as tar:
        tar.extractall(path=target_dir)

# ════════════════════════════════════════
# 🗺️ HTML to Route Mapping
# ════════════════════════════════════════
@auto_model
@auto_route
@auto_logic
def get_template_routes_map(template_dir: str, route_dir: str) -> dict:
    # Maps base template file to all routes that render it
    route_map = {}
    for dirpath, _, filenames in os.walk(route_dir):
        for f in filenames:
            if not f.endswith('.py'): continue
            full_path = os.path.join(dirpath, f)
            with open(full_path, 'r', encoding='utf-8') as fp:
                code = fp.read()
                for line in code.splitlines():
                    if "render_template" in line or "TemplateResponse" in line:
                        for html_file in os.listdir(template_dir):
                            if html_file in line:
                                route_map.setdefault(html_file, []).append(full_path)
    return route_map

