# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
print("[OK] generate_function_usage_map.py imported")

from handler import auto_logic
from handler import auto_route
from handler import auto_model
import os
import json

from odil.generate_model_trace import generate_model_trace
from odil.generate_logic_trace import generate_logic_trace
from odil.generate_function_usage_map import generate_function_usage_map
from odil.generate_route_trace import generate_route_trace
from odil.generate_template_trace import generate_template_trace

# ✅ Clean path block
BASE_DIR = os.path.abspath(os.path.dirname(__file__))           # tools/devops
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))     # root/smartswasthya
ODIL_DIR = os.path.join(PROJECT_DIR, "odil")                    # root/smartswasthya/odil

OUTPUT_FILE = os.path.join(PROJECT_DIR, "circuit_trace.json")


@auto_model
@auto_route
@auto_logic
def normalize_entry(src, dst):
    if not src or not dst:
        return None
    if isinstance(dst, list):  # ✅ flatten all destination values if list
        return [{"source": src.strip(), "target": d.strip()} for d in dst if isinstance(d, str)]
    if isinstance(dst, str):
        return {"source": src.strip(), "target": dst.strip()}
    return None


@auto_model
@auto_route
@auto_logic
def build_circuit_trace():
    print("⚙️ Running live trace generators...")

    model_data     = generate_model_trace()
    print(f"📥 model_data → {type(model_data)} ({len(model_data) if model_data else 0})")

    logic_data     = generate_logic_trace()
    print(f"📥 logic_data → {type(logic_data)} ({len(logic_data) if logic_data else 0})")

    function_data  = generate_function_usage_map()
    print(f"📥 function_data → {type(function_data)} ({len(function_data) if function_data else 0})")

    route_data     = generate_route_trace()
    print(f"📥 route_data → {type(route_data)} ({len(route_data) if route_data else 0})")

    template_data  = generate_template_trace()
    print(f"📥 template_data → {type(template_data)} ({len(template_data) if template_data else 0})")

    full_trace = []

    @auto_model
    @auto_route
    @auto_logic
    def add(src, dst):
        if not src or not dst:
            return
        if isinstance(dst, list):
            for d in dst:
                if isinstance(d, str):
                    full_trace.append({"source": src.strip(), "target": d.strip()})
        elif isinstance(dst, str):
            full_trace.append({"source": src.strip(), "target": dst.strip()})

    # ✅ 1. Model → Model (if list of strings, build sequential pairs)
    if isinstance(model_data, list):
        if all(isinstance(e, str) for e in model_data):
            for i in range(len(model_data) - 1):
                add(model_data[i], model_data[i + 1])
        else:
            for entry in model_data:
                if isinstance(entry, dict):
                    add(entry.get("source") or entry.get("caller"), entry.get("target") or entry.get("callee"))

    # ✅ 2. Logic → Model
    if isinstance(logic_data, list):
        for entry in logic_data:
            if isinstance(entry, dict):
                add(entry.get("source") or entry.get("caller"), entry.get("target") or entry.get("callee"))

    # ✅ 3. Function → Logic
    if isinstance(function_data, list):
        for entry in function_data:
            if isinstance(entry, dict):
                add(entry.get("source") or entry.get("caller"), entry.get("target") or entry.get("callee"))

    # ✅ 4. Route → Function
    if isinstance(route_data, list):
        for entry in route_data:
            if isinstance(entry, dict):
                add(entry.get("source") or entry.get("caller"), entry.get("target") or entry.get("callee"))

    # ✅ 5. Template → Route
    if isinstance(template_data, list):
        for entry in template_data:
            if isinstance(entry, dict):
                add(entry.get("source") or entry.get("caller"), entry.get("target") or entry.get("callee"))

    # ✅ 6. Docker-level: Extract from tools/devops/chain_tracer.py
    from tools.devops.chain_tracer import extract_all_routes
    docker_routes = extract_all_routes()
    for method, route_path, file_path in docker_routes:
        add(f"Docker:{file_path.name}", f"Route:{route_path}")

    # ✅ 7. Celery/Startup-level: Trace from prelaunch_checker_v3.py
    from tools.prelaunch_checker_v3 import scan_dynamic_imports, scan_router_chain
    for path, lineno, line in scan_dynamic_imports():
        add("Startup:DynamicImport", f"{path}#{lineno}")
    if scan_router_chain() > 0:
        add("Startup:IncludeRouterChain", "Route:MultiInclude")

    # ✅ Final loop: Add again normalized links to ensure all formats are caught
    for trace_list in [model_data, logic_data, function_data, route_data, template_data]:
        for entry in (trace_list.items() if isinstance(trace_list, dict) else trace_list):
            if isinstance(entry, tuple):
                src, dst = entry
            else:
                src = entry.get("source") or entry.get("caller")
                dst = entry.get("target") or entry.get("callee")
            norm = normalize_entry(src, dst)
            if isinstance(norm, list):
                full_trace.extend(norm)
            elif norm:
                full_trace.append(norm)

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(full_trace, f, indent=2)
        print(f"✅ circuit_trace.json saved at: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Could not write circuit_trace.json — {e}")

    return full_trace


if __name__ == "__main__":
    print("🔌 Generating full circuit_trace.json (live run)...")
    circuit = build_circuit_trace()
    print(f"➕ Total links: {len(circuit)}")
