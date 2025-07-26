# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_logic, auto_function
from tools.obvious_router import auto_function as obs_func
from handler import auto_logic, auto_route, auto_model

import sys, os
from pathlib import Path
import json
from tools.smart_logger import SmartLogger

# 🧭 Path Setup
PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 📦 Logger
logger = SmartLogger("InstructionLogic")

# 📁 File Path
INSTRUCTION_JSON = Path(PROJECT_ROOT) / "dev_data" / "instructions.json"

# 🔁 Run Logic
@auto_model
@auto_route
@auto_logic
def run(*args, **kwargs):
    logger.info("Running logic: instruction_logic.run()")
    try:
        if not INSTRUCTION_JSON.exists():
            logger.warning("instructions.json not found.")
            return {"instructions": []}
        with open(INSTRUCTION_JSON, "r", encoding="utf-8") as f:
            instructions = json.load(f)
        logger.info(f"Loaded {len(instructions)} instructions.")
        return {"instructions": instructions}
    except Exception as e:
        logger.error(f"Run error: {str(e)}")
        return {"status": "error", "message": str(e)}

# 📝 Apply Logic
@auto_model
@auto_route
@auto_logic
def apply(instruction: dict = None):
    logger.info("Running logic: instruction_logic.apply()")
    try:
        if not instruction or not isinstance(instruction, dict):
            return {"status": "error", "message": "No valid instruction provided"}

        instructions = []
        if INSTRUCTION_JSON.exists():
            with open(INSTRUCTION_JSON, "r", encoding="utf-8") as f:
                instructions = json.load(f)

        instructions.append(instruction)

        with open(INSTRUCTION_JSON, "w", encoding="utf-8") as f:
            json.dump(instructions, f, indent=2)

        logger.info(f"Instruction added: {instruction.get('title', 'Untitled')}")
        return {"status": "applied", "instruction_count": len(instructions)}
    except Exception as e:
        logger.error(f"Apply error: {str(e)}")
        return {"status": "error", "message": str(e)}
