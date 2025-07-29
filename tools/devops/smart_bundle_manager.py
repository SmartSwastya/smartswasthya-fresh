# Replace import toml with import tomllib, and load with tomllib.load (binary mode)

updated_smart_bundle_manager = """
# ========================== SMART BUNDLE MANAGER SYSTEM ==========================
# Filename: tools/devops/smart_bundle_manager.py
# Purpose : Auto-manage tar.gz based package bundles for Dockerfile.pkggen builds
# Author  : Auto-generated via ChatGPT x Hrushikesh Collab
# ================================================================================

# tools/devops/smart_bundle_manager.py

import os
import sys
import json
import shutil
import subprocess
import tarfile
import argparse
import tomllib  # Use stdlib tomllib instead of toml
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ================== CONFIG =====================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
WHEEL_DIR = PROJECT_ROOT / "tarstack/buildtools/python_wheels"
TAR_OUTPUT = PROJECT_ROOT / "tarstack/buildtools/python_packages.tar.gz"
MANIFEST_PATH = PROJECT_ROOT / "tools/devops/installed_manifest.json"
LOG_DIR = PROJECT_ROOT / "tools/devops/bundle_update_logs"

# Ensure log dir
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ============== UTILITY FUNCS ===================

def parse_pyproject():
    with open(PYPROJECT_PATH, "rb") as f:  # Binary mode for tomllib
        pyproject = tomllib.load(f)
    deps = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
    print("📦 Dependencies Parsed:", deps)
    return deps

def read_manifest():
    if not MANIFEST_PATH.exists():
        return {}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def write_manifest(manifest):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

def log_bundle_update(log_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"bundle_update_{timestamp}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

def clean_win_wheels():
    for f in WHEEL_DIR.glob("*win_amd64*.whl"):
        f.unlink()

def deduplicate_wheels():
    pkgs = defaultdict(list)
    for f in WHEEL_DIR.glob("*.whl"):
        pkg = f.name.split("-")[0]
        pkgs[pkg].append(f)

    for files in pkgs.values():
        if len(files) > 1:
            files.sort()
            for f in files[:-1]:  # keep only latest
                f.unlink()

def install_wheels(deps: dict):
    reqs = [f"{k}=={v.lstrip('^')}" for k, v in deps.items() if k.lower() != "python"]
    subprocess.run([
        sys.executable, "-m", "pip", "download",
        "--only-binary=:all:",
        "--platform", "manylinux2014_x86_64",
        "--implementation", "cp",
        "--abi", "cp311",
        "--python-version", "3.11",
        "--no-deps",
        "--dest", WHEEL_DIR,  # ✅ FIXED here
    ] + reqs, check=True)

def rebuild_tar():
    if TAR_OUTPUT.exists():
        TAR_OUTPUT.unlink()
    with tarfile.open(TAR_OUTPUT, "w:gz") as tar:
        for file in WHEEL_DIR.glob("*.whl"):
            if (
                "win_amd64" not in file.name and
                "macosx" not in file.name and
                "any" in file.name or "manylinux" in file.name
            ):
                tar.add(file, arcname=file.name)

def update_manifest_from_dir(manifest):
    for file in WHEEL_DIR.glob("*.whl"):
        parts = file.name.split("-")
        name = parts[0].lower()
        version = parts[1] if len(parts) > 1 else "unknown"
        manifest[name] = {
            "version": version,
            "type": "python",
            "updated_at": datetime.now().isoformat()
        }
    return manifest

# ============== CORE COMMANDS ===================

def auto_refresh():
    print("🔄 Refreshing full bundle from pyproject.toml...")
    deps = parse_pyproject()
    install_wheels(deps)
    clean_win_wheels()
    deduplicate_wheels()
    rebuild_tar()
    manifest = update_manifest_from_dir({})
    write_manifest(manifest)
    log_bundle_update({
        "mode": "refresh",
        "downloaded": deps,
        "total": len(manifest),
        "timestamp": datetime.now().isoformat()
    })
    print("✅ Bundle refreshed.")

def verify_bundle():
    manifest = read_manifest()
    expected = set(manifest.keys())
    actual = set(f.name.split("-")[0].lower() for f in WHEEL_DIR.glob("*.whl"))
    missing = expected - actual
    if missing:
        print("❌ Missing packages:", ", ".join(sorted(missing)))
        return False
    print("✅ All wheels present.")
    return True

def add_packages(pkg_list):
    print(f"➕ Adding: {', '.join(pkg_list)}")
    install_wheels(pkg_list)
    clean_win_wheels()
    deduplicate_wheels()
    rebuild_tar()
    manifest = read_manifest()
    manifest = update_manifest_from_dir(manifest)
    write_manifest(manifest)
    log_bundle_update({
        "mode": "add",
        "added": pkg_list,
        "total": len(manifest),
        "timestamp": datetime.now().isoformat()
    })
    print("✅ Package(s) added.")

# ============== CLI ENTRYPOINT ===================

def main():
    parser = argparse.ArgumentParser(description="Smart Python bundle manager")
    parser.add_argument("--refresh", action="store_true", help="Force rebuild from pyproject.toml")
    parser.add_argument("--verify", action="store_true", help="Validate wheels in bundle")
    parser.add_argument("--add", nargs="+", help="Add extra package(s)")

    args = parser.parse_args()

    if args.refresh:
        auto_refresh()
    elif args.verify:
        verify_bundle()
    elif args.add:
        add_packages(args.add)
    else:
        if not TAR_OUTPUT.exists():
            print("📦 Tarball missing. Rebuilding...")
            auto_refresh()
        else:
            print("✅ Bundle tar exists. Use --refresh to force rebuild.")

if __name__ == "__main__":
    main()
"""

# Apply: tools/devops/smart_bundle_manager.py मध्ये हे paste कर. pyproject.toml मधून toml dependency काढ (tomllib stdlib आहे).