# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# 🧠 GPT PROMPT GENERATOR
# 📁 File: tools/gpt_prompt_generator.py
# 🔧 Purpose: Generates a GPT-friendly prompt for a dev task
# Uses ODIL trace JSONs to gather context for ChatGPT assistance
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

import json
from pathlib import Path
from tools.smart_logger import SmartLogger

logger = SmartLogger("gpt_prompt_generator")
ODIL_DIR = Path("smartswasthya/odil")

@auto_model
@auto_route
@auto_logic
def read_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"❌ Error reading {file_path}: {e}")
        return {}

@auto_model
@auto_route
@auto_logic
def generate_prompt(task_id: str, route_name: str) -> str:
    model_trace = read_json(ODIL_DIR / "model_trace.json")
    function_trace = read_json(ODIL_DIR / "function_trace.json")
    logic_trace = read_json(ODIL_DIR / "logic_trace.json")
    route_trace = read_json(ODIL_DIR / "route_trace.json")
    template_trace = read_json(ODIL_DIR / "template_trace.json")

    connected_models = model_trace.get(route_name, [])
    connected_functions = function_trace.get(route_name, [])
    logic_blocks = logic_trace.get(route_name, [])
    template_used = template_trace.get(route_name, [])

    prompt = f"""🧠 GPT AUTO-PROMPT (Task ID: {task_id})

You're helping implement a Smart Swasthya Seva task connected to: `{route_name}`

🎯 Connected Context:
- Models involved: {', '.join(connected_models) if connected_models else 'N/A'}
- Functions used: {', '.join(connected_functions) if connected_functions else 'N/A'}
- Logic files impacted: {', '.join(logic_blocks) if logic_blocks else 'N/A'}
- Template files: {', '.join(template_used) if template_used else 'N/A'}

📌 Goal: Write or refactor logic, models, routes, or templates as per above context.
You can now ask specific implementation queries.
"""

    logger.success(f"Prompt generated for {route_name} (Task: {task_id})")
    return prompt

# 🧪 Optional test
if __name__ == "__main__":
    example_prompt = generate_prompt("TASK_102", "sync_results_routes.py")
    print(example_prompt)

