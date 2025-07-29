# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ╭────────────────────────────────────────────────────────────╮
# │ 📦 TOOL WRAPPER :: developer_task_loader.py               │
# │ Description: Load developer task instructions from JSON   │
# ╰────────────────────────────────────────────────────────────╯

import json
import os

INSTRUCTION_FILE = os.path.join(os.path.dirname(__file__), "instructions.json")

# ╭────────────────────────────────────────────────────────────╮
# │ 📤 Load all instructions from file                         │
# ╰────────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def load_all_instructions():
    if not os.path.exists(INSTRUCTION_FILE):
        return []

    with open(INSTRUCTION_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# ╭────────────────────────────────────────────────────────────╮
# │ 🔢 Fetch single task by index                              │
# ╰────────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def get_instruction_by_index(index):
    instructions = load_all_instructions()
    if 0 <= index < len(instructions):
        return instructions[index]
    return {"error": "Invalid index"}

# ╭────────────────────────────────────────────────────────────╮
# │ 🆕 Generate dev_bucket_submissions.json from instructions  │
# ╰────────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def generate_dev_bucket_submission(output_file="../dev_data/dev_bucket_submissions.json"):
    instructions = load_all_instructions()
    if not instructions:
        print("⚠️ No instructions found. Cannot generate submissions.")
        return

    submission_data = []
    for i, task in enumerate(instructions):
        submission_data.append({
            "task_id": f"task_{i+1:03}",
            "title": task.get("name", "Untitled Task"),
            "description": task.get("input_desc", "No description provided."),
            "type": task.get("type", "misc"),
            "section": task.get("type", "misc"),
            "priority": task.get("priority", "Medium"),
            "required_files": [f.strip() for f in task.get("required_files", [])],
            "assigned_to": "auto_system",
            "status": "pending"
        })

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(submission_data, f, indent=2)
    print(f"✅ Dev Bucket submission file written to: {output_file}")

# ╭────────────────────────────────────────────────────────────╮
# │ 🚀 CLI testing (Optional)                                 │
# ╰────────────────────────────────────────────────────────────╯
if __name__ == "__main__":
    print("📦 Developer Task Loader")
    all_instructions = load_all_instructions()

    if not all_instructions:
        print("⚠️ No instructions found.")
    else:
        for i, inst in enumerate(all_instructions):
            print(f"\n🔢 Task {i + 1}: {inst['name']} — {inst['type']}")
            print(f"   Files: {', '.join(inst['required_files'])}")

