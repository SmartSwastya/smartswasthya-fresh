# 📦 Plugin module for SmartEngine
# 🔧 Scans common structural or utility issues
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def scan_missing_init_py():
    missing_init = []
    for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
        skip = any(p in dirpath for p in ['.git', '.idea', '__pycache__', 'venv', 'tarstack', 'node_modules'])
        if skip:
            continue
        if '__init__.py' not in filenames:
            if any(f.endswith('.py') for f in filenames):
                rel_path = os.path.relpath(dirpath, PROJECT_ROOT)
                missing_init.append(rel_path)
    return missing_init

def check_static_folder():
    static_path = os.path.join(PROJECT_ROOT, "static")
    result = {
        "exists": os.path.exists(static_path),
        "has_css": False,
        "has_js": False,
        "has_images": False
    }
    if os.path.isdir(static_path):
        for root_dir, dirs, files in os.walk(static_path):
            for file in files:
                if file.endswith(".css"):
                    result["has_css"] = True
                elif file.endswith(".js"):
                    result["has_js"] = True
                elif file.lower().endswith((".png", ".jpg", ".jpeg", ".svg")):
                    result["has_images"] = True
            break
    return result

def check_essential_folders():
    essentials = ["templates", "routes", "models", "tools"]
    missing = []
    for folder in essentials:
        if not os.path.exists(os.path.join(PROJECT_ROOT, folder)):
            missing.append(folder)
    return missing

def check_python_wheels():
    """
    Check if python_wheels/ exists and contains .whl files.
    Also verify python_packages.tar.gz exists (used in Docker build stage).
    """
    wheels_dir = os.path.join(PROJECT_ROOT, "tarstack", "buildtools", "python_wheels")
    tarball_path = os.path.join(PROJECT_ROOT, "tarstack", "buildtools", "python_packages.tar.gz")

    result = {
        "wheels_dir_exists": os.path.isdir(wheels_dir),
        "wheel_files": [],
        "tarball_exists": os.path.isfile(tarball_path)
    }

    if result["wheels_dir_exists"]:
        result["wheel_files"] = sorted([
            f for f in os.listdir(wheels_dir) if f.endswith(".whl")
        ])

    return result
