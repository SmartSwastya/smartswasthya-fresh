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
import ast
import json
from pathlib import Path

ROUTES_DIR = Path(__file__).parent.parent / "routes"
OUTPUT_FILE = Path(__file__).parent.parent / "route_trace.json"

@auto_model
@auto_route
@auto_logic
def extract_routes_from_file(file_path: Path) -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    routes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    func = decorator.func
                    if isinstance(func, ast.Attribute):
                        if getattr(func.value, 'id', None) == 'router' and func.attr in ['get', 'post', 'put', 'delete', 'patch']:
                            if decorator.args and isinstance(decorator.args[0], ast.Constant):
                                route_path = decorator.args[0].value
                                routes.append({
                                    "source": route_path,
                                    "target": function_name,
                                    "file": str(file_path)
                                })
    return routes

@auto_model
@auto_route
@auto_logic
def generate_route_trace() -> list:
    trace = []
    for file_path in ROUTES_DIR.rglob("*.py"):
        trace.extend(extract_routes_from_file(file_path))
    return trace

if __name__ == "__main__":
    output = generate_route_trace()
    print(f"Route-handler pairs: {len(output)}")
    for entry in output[:5]:
        print(entry)

    # Save to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"[OK] route_trace.json saved at: {OUTPUT_FILE}")
