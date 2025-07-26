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

TRACE_DEBUG = False

from odil.generate_function_usage_map import generate_function_usage_map as gen_func_map
from odil.generate_model_trace import main as gen_model_trace
from odil.generate_logic_trace import main as gen_logic_trace
from odil.generate_code_trace import main as gen_code_trace

@auto_model
@auto_route
@auto_logic
def save_trace_log(content: str, filename: str = "trace_runner_summary.txt"):
    primary_path = os.path.join("records", filename)
    try:
        with open(primary_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Trace runner log saved to: {primary_path}")
    except PermissionError:
        print(f"⚠️ Permission denied at {primary_path}, trying fallback...")

        fallback_dir = ".internal_logs"
        os.makedirs(fallback_dir, exist_ok=True)
        fallback_path = os.path.join(fallback_dir, filename)
        try:
            with open(fallback_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Trace runner log saved to fallback: {fallback_path}")
        except Exception as e:
            print(f"❌ Failed to save fallback trace log: {e}")

@auto_model
@auto_route
@auto_logic
def run_trace_generators_with_log():
    summary_lines = []

    @auto_model
    @auto_route
    @auto_logic
    def debug(msg):
        if TRACE_DEBUG:
            print(msg)
        summary_lines.append(msg)

    debug("🧠 Starting full trace generator batch...")

    try:
        debug("\n▶ Running: odil/generate_function_usage_map.py")
        gen_func_map()
    except Exception as e:
        debug(f"❌ Error in function usage map: {e}")

    try:
        debug("\n▶ Running: odil/generate_model_trace.py")
        gen_model_trace()
    except Exception as e:
        debug(f"❌ Error in model trace: {e}")

    try:
        debug("\n▶ Running: odil/generate_logic_trace.py")
        gen_logic_trace()
    except Exception as e:
        debug(f"❌ Error in logic trace: {e}")

    try:
        debug("\n▶ Running: odil/generate_code_trace.py")
        gen_code_trace()
    except Exception as e:
        debug(f"❌ Error in code trace: {e}")

    debug("\n✅ All trace generators executed.")

    save_trace_log("\n".join(summary_lines))

if __name__ == "__main__":
    run_trace_generators_with_log()

