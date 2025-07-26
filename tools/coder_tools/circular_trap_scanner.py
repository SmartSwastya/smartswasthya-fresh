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
from collections import defaultdict, deque
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
TARGET_DIR = BASE_DIR / "smartswasthya"
LOG_DIR = BASE_DIR / "records" / "circular_trap_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

GRAPH = defaultdict(set)
VISITED_FILES = {}
CIRCULAR_PATHS = []

@auto_model
@auto_route
@auto_logic
def find_py_files(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        if any(skip in dirpath for skip in ['__pycache__', '.git', '.venv']):
            continue
        for file in filenames:
            if file.endswith('.py'):
                yield os.path.join(dirpath, file)

@auto_model
@auto_route
@auto_logic
def parse_imports(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports
    except Exception:
        return []

@auto_model
@auto_route
@auto_logic
def normalize_path(path):
    return os.path.relpath(path, TARGET_DIR).replace(os.sep, ".").rstrip(".py")

@auto_model
@auto_route
@auto_logic
def build_graph():
    for py_file in find_py_files(TARGET_DIR):
        mod_name = normalize_path(py_file)
        imports = parse_imports(py_file)
        VISITED_FILES[mod_name] = py_file
        for imp in imports:
            if imp.startswith("smartswasthya"):
                GRAPH[mod_name].add(imp)

@auto_model
@auto_route
@auto_logic
def detect_cycles():
    visited = set()
    stack = []

    @auto_model
    @auto_route
    @auto_logic
    def dfs(node, path):
        visited.add(node)
        path.append(node)

        for neighbor in GRAPH.get(node, []):
            if neighbor in path:
                idx = path.index(neighbor)
                cycle = path[idx:] + [neighbor]
                if cycle not in CIRCULAR_PATHS:
                    CIRCULAR_PATHS.append(cycle)
            elif neighbor not in visited:
                dfs(neighbor, path)

        path.pop()

    for mod in GRAPH:
        dfs(mod, [])

@auto_model
@auto_route
@auto_logic
def report_results():
    log_file = LOG_DIR / "circular_trap_report.log"
    with open(log_file, "w", encoding="utf-8") as f:
        if CIRCULAR_PATHS:
            print("🚨 Circular Imports Detected:")
            for cycle in CIRCULAR_PATHS:
                cycle_str = " ➜ ".join(cycle)
                print(f"🔁 {cycle_str}")
                f.write(f"{cycle_str}\n")
        else:
            print("✅ No circular imports detected.")
            f.write("✅ No circular imports detected.\n")
    print(f"📄 Full report saved: {log_file}")

@auto_model
@auto_route
@auto_logic
def run_circular_trap_scan():
    print("🧠 Running Circular Trap Scanner...")
    build_graph()
    detect_cycles()
    report_results()

if __name__ == "__main__":
    run_circular_trap_scan()

