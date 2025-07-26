"""
📦 SmartEngine.py v2 — Production Grade Rewrite
- Mirrors actual main.py setup flow
- Validates real route, template, and model linkage
- Preserves original debugging menu style
"""

import os
import ast
import sys
from pathlib import Path
from fastapi.routing import APIRoute
from fastapi.templating import Jinja2Templates
from types import ModuleType

# Load actual FastAPI app
try:
    from main import app
except ImportError:
    print("❌ ERROR: main.py not found or app not importable.")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).parent.resolve()
TEMPLATES_DIR = PROJECT_ROOT / "templates"
ROUTES_DIR = PROJECT_ROOT / "routes"
MODELS_DIR = PROJECT_ROOT / "models"

# -----------------------------
# 🔍 ROUTE ANALYSIS
# -----------------------------
def get_registered_template_files():
    found_templates = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            response_class = getattr(route, "response_class", None)
            if response_class and getattr(response_class, "__name__", "") == "HTMLResponse":
                source = route.endpoint.__code__.co_consts
                for const in source:
                    if isinstance(const, str) and const.endswith(".html"):
                        found_templates.add(const)
    return found_templates

def get_all_template_files():
    return {f.name for f in TEMPLATES_DIR.glob("*.html")}


def get_all_route_files():
    return list(ROUTES_DIR.rglob("*.py"))


# -----------------------------
# 🧬 MODEL ANALYSIS
# -----------------------------
def find_model_classes(path: Path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if hasattr(base, "id") and base.id == "Base":
                        return True
    except Exception:
        return False
    return False


def check_models():
    flagged = []
    for path in MODELS_DIR.rglob("*.py"):
        if find_model_classes(path):
            content = path.read_text(encoding="utf-8")
            if "@auto_model" not in content or "def get_model" not in content:
                flagged.append(str(path.relative_to(PROJECT_ROOT)))
    return flagged


# -----------------------------
# 🔍 TEMPLATE DIAGNOSTICS
# -----------------------------
def check_templates():
    import inspect
    import re
    from fastapi.routing import APIRoute
    from starlette.templating import _TemplateResponse as TemplateResponse

    rendered_templates = set()
    patterns = [
        r'TemplateResponse\(["\']([^"\']+.html)["\']',
        r'templates\.TemplateResponse\(["\']([^"\']+.html)["\']',
        r'render_template\(["\']([^"\']+.html)["\']',
        r'Page\(["\']([^"\']+.html)["\']',
    ]

    for route in app.routes:
        if isinstance(route, APIRoute):
            try:
                source = inspect.getsource(route.endpoint)
                for pattern in patterns:
                    for match in re.findall(pattern, source):
                        rendered_templates.add(match)
            except Exception:
                continue

    all_templates = {f.name for f in TEMPLATES_DIR.glob("*.html")}
    ghost_templates = sorted(all_templates - rendered_templates)
    return ghost_templates


# -----------------------------
# ⚙️ ROUTE DIAGNOSTICS (REWRITE)
# -----------------------------
def check_routes():
    missing_auto = []
    for path in get_all_route_files():
        try:
            content = path.read_text(encoding="utf-8")
            has_decorator = "@auto_route" in content
            has_router = "router =" in content or "APIRouter()" in content
            has_get_router = "def get_router" in content
            if not (has_decorator or has_get_router or has_router):
                rel_path = str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
                missing_auto.append(rel_path)
        except Exception:
            continue
    return missing_auto


def check_main_registered_routes():
    registered_paths = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            registered_paths.add(route.path)
    return registered_paths


# -----------------------------
# 🧪 DIAGNOSTIC MENU
# -----------------------------
def show_menu():
    model_issues = check_models()
    route_issues = check_routes()
    ghost_templates = check_templates()
    registered_routes = check_main_registered_routes()

    print("\n🔧 SmartEngine Digest Scanner Started...\n")
    print("📦 File Groups Scanned:\n")
    print(f"  [models    ] → {len(list(MODELS_DIR.rglob('*.py')))} files")
    print(f"  [routes    ] → {len(list(ROUTES_DIR.rglob('*.py')))} files")
    print(f"  [templates ] → {len(list(TEMPLATES_DIR.glob('*.html')))} files\n")

    issues = {
        1: ("[models] - missing @auto_model marker", model_issues),
        2: ("[routes] - missing @auto_route marker", route_issues),
        3: ("[templates] - no render route found (ghost?)", ghost_templates),
    }

    print("⚠️ Detected Issues (Grouped):\n")
    for k, (desc, arr) in issues.items():
        if arr:
            print(f"  [{k}] 🧬 {desc} → {len(arr)}")
    print("\n🔎 Enter issue number to expand [1–3], or press ENTER to exit:")

    try:
        choice = input("> ").strip()
        if choice in ["1", "2", "3"]:
            index = int(choice)
            _, items = issues[index]
            print("\n📂 Details:\n")
            for i in items:
                print(f"   • {i}")
    except KeyboardInterrupt:
        print("\n👋 Exiting.")


if __name__ == "__main__":
    show_menu()
