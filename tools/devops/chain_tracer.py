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
import ast
import json
from pathlib import Path
from datetime import datetime

from tools.obvious_router_registrar import register_all_routes
from odil.generate_model_trace import generate_model_trace

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
MODELS_DIR = BASE_DIR / "models"
RECORD_DIR = BASE_DIR / "records" / "chain_logs"
RECORD_DIR.mkdir(parents=True, exist_ok=True)

REPORT_LINES = []

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
def find_all_templates():
    return list(TEMPLATE_DIR.rglob("*.html"))

@auto_model
@auto_route
@auto_logic
def extract_api_calls_from_html(html_path):
    apis = []
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
            fetch_calls = re.findall(r"fetch\(['\"](.*?)['\"]", content)
            ajax_calls = re.findall(r"\$\.(get|post|put|delete)\(['\"](.*?)['\"]", content)
            onclick_calls = re.findall(r'onclick=["\'].*?(\/[a-zA-Z0-9_\-/]+).*?["\']', content)
            apis.extend(fetch_calls)
            apis.extend(url for _, url in ajax_calls)
            apis.extend(onclick_calls)
    except Exception as e:
        log(f"❌ Error reading {html_path}: {e}")
    return list(set(apis))

@auto_model
@auto_route
@auto_logic
def extract_all_routes():
    all_routes = []
    try:
        routers = register_all_routes()
        for entry in routers:
            router = entry.get("router")
            source = entry.get("source")
            if router and hasattr(router, "routes"):
                for route in router.routes:
                    methods = route.methods or {"GET"}
                    path = route.path
                    if hasattr(route, "endpoint") and hasattr(route.endpoint, "__code__"):
                        filename = Path(route.endpoint.__code__.co_filename)
                        for method in methods:
                            all_routes.append((method.upper(), path, filename))
    except Exception as e:
        log(f"❌ Error in extracting routes via registrar: {e}")
    return all_routes

@auto_model
@auto_route
@auto_logic
def match_route(api_path, all_routes):
    matched = []
    for method, route_path, file in all_routes:
        if route_path.strip("/") == api_path.strip("/"):
            matched.append((method, route_path, file))
    return matched

@auto_model
@auto_route
@auto_logic
def find_logic_function(route_file, route_path):
    try:
        with open(route_file, "r", encoding="utf-8") as f:
            node = ast.parse(f.read())
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    for decorator in item.decorator_list:
                        if isinstance(decorator, ast.Call):
                            if hasattr(decorator.func, 'attr') and decorator.func.attr in ("get", "post", "put", "delete"):
                                args = [a.s for a in decorator.args if isinstance(a, ast.Constant)]
                                if route_path in args:
                                    return item.name
    except Exception as e:
        log(f"❌ Error parsing AST in {route_file}: {e}")
    return None

@auto_model
@auto_route
@auto_logic
def find_models_in_function(logic_file, function_name):
    models_used = set()
    try:
        with open(logic_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.Name):
                            if subnode.id[0].isupper():
                                models_used.add(subnode.id)
    except Exception as e:
        log(f"❌ Error in logic scan {logic_file}: {e}")
    return models_used

generate_model_trace()  # This will load all models into Base.__subclasses__()
ALL_MODEL_CLASSES = {cls.__name__ for cls in Base.__subclasses__()}

@auto_model
@auto_route
@auto_logic
def check_model_exists(model_name):
    return model_name in ALL_MODEL_CLASSES

@auto_model
@auto_route
@auto_logic
def run_chain_trace():
    section("🔗 Smart Dev Full Chain Tracer (HTML → API → Logic → Model)")
    html_files = find_all_templates()
    all_routes = extract_all_routes()

    for html_file in html_files:
        log(f"\n📄 Template: {html_file.relative_to(TEMPLATE_DIR)}")
        apis = extract_api_calls_from_html(html_file)
        if not apis:
            log("  ⚠️ No API calls found in template.")
            continue

        for api in apis:
            log(f" ↳ API: {api}")
            matched_routes = match_route(api, all_routes)
            if not matched_routes:
                log("    ❌ No route found")
                continue

            for method, route_path, route_file in matched_routes:
                log(f"    ✔ Route: {method} {route_path} in {route_file.name}")
                logic_func = find_logic_function(route_file, route_path)
                if not logic_func:
                    log("      ⚠️ Logic function not found or unnamed")
                    continue

                log(f"      ✔ Logic Function: {logic_func}")
                models = find_models_in_function(route_file, logic_func)
                if not models:
                    log("        ⚠️ No model usage detected")
                else:
                    for model in models:
                        exists = check_model_exists(model)
                        status = "✔" if exists else "❌"
                        log(f"        {status} Model: {model}")
    return

@auto_model
@auto_route
@auto_logic
def save_report():
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = RECORD_DIR / f"chain_report_{ts}.log"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(REPORT_LINES))
    log(f"\n📝 Full report saved to: {path}")

if __name__ == "__main__":
    run_chain_trace()
    save_report()
