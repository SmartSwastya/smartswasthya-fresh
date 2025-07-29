# tools/run_all_trace_generators.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import subprocess
import sys
import os
import time
from pathlib import Path
from tools.smart_logger import SmartLogger
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function

logger = SmartLogger("TraceRunner")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

TRACE_SCRIPTS = [
    "odil/generate_model_trace.py",                # ✅ Base
    "odil/generate_logic_trace.py",                # ✅ Base
    "odil/generate_code_trace.py",                 # ✅ Creates function_trace.json
    "odil/generate_function_usage_map.py",         # 🔄 Uses function_trace.json
    "odil/generate_route_trace.py",                # ✅ Independent
    "odil/generate_template_trace.py",             # ✅ Independent
    "odil/generate_obvious_connections.py",        # 🔄 Needs model/logic/function usage
    "odil/generate_blueprint_compliance.py",       # 🔄 Needs route/function/logic
    "tools/devops/generate_circuit_trace.py",      # 🔄 Final summary
    "tools/ammeter.py",                            # ✅ Ammeter diagnostic
]

def run_script(script_path: str):
    full_path = PROJECT_ROOT / script_path
    logger.log_info("Trace", script_path, "▶ Running...")
    print(f"\n📦 Running: {script_path}")

    start = time.time()

    try:
        result = subprocess.run(
            [sys.executable, str(full_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        elapsed = round(time.time() - start, 2)

        if result.returncode == 0:
            logger.log_success("Trace", script_path, f"✅ Success ({elapsed}s)")
            if result.stdout.strip():
                print(result.stdout.strip())
        else:
            logger.log_error("Trace", script_path, f"❌ Failed ({elapsed}s)")
            print(result.stderr.strip())

    except Exception as e:
        logger.log_critical("Trace", script_path, f"💥 Exception: {e}")
        print(f"💥 Error while running {script_path}: {e}")

def run_all_traces():
    print("\n🔁 Starting all trace generators...\n" + "-" * 40)
    for script in TRACE_SCRIPTS:
        run_script(script)
    print("\n✅ All trace generators completed.\n" + "-" * 40)

if __name__ == "__main__":
    run_all_traces()
