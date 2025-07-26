# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ╔════════════════════════════════════════════════════════════╗
# ║ 📌 instruction_editor.py — Instruction Entry CLI Tool     ║
# ║ CLI interface to build instructions & task definitions    ║
# ╚════════════════════════════════════════════════════════════╝

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from tools.edit_logger import log_instruction_edit

# 🔧 Allow importing from parent directory
PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# from logic.instruction_logic import (
#     generate_instruction,
#     save_instruction_set,
#     build_sample_instruction_set
# )

# ╔════════════════════════════╗
# ║ 🔧 Configuration Constants ║
# ╚════════════════════════════╝
BASE_DIR_TOOLS = str(Path(__file__).resolve().parent)
BASE_DIR_DEV_BUCKET = str(Path(BASE_DIR_TOOLS).parent / "dev_bucket")

INSTRUCTION_FILE   = os.path.join(BASE_DIR_TOOLS, "instructions.json")
ADMIN_REVIEW_FILE  = os.path.join(BASE_DIR_DEV_BUCKET, "admin_review_queue.json")
FINAL_FILE         = os.path.join(BASE_DIR_DEV_BUCKET, "final_task_queue.json")
REJECTED_FILE      = os.path.join(BASE_DIR_DEV_BUCKET, "rejected_task_queue.json")

# ╔═════════════════════════════════════════════╗
# ║ 🧠 CLI: Build New Custom Instruction Entry  ║
# ╚═════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
def create_custom_instruction():
# @auto_flag: input_shell [input(]
# ⚠️ input() or shell call found — sanitize required
# @auto_flag: input_shell [input(]
# ⚠️ input() or shell call found — sanitize required
# @auto_flag: input_shell [input(]
# ⚠️ input() or shell call found — sanitize required
    print("📝 Task Name:", end=" "); task_name = input().strip()
    print("📂 Task Type (route/frontend/backend/etc.):", end=" "); task_type = input().strip()
    print("📥 Input Data Description:", end=" "); input_desc = input().strip()
    print("📤 Output Result Description:", end=" "); output_desc = input().strip()
    print("📁 Required Files (comma separated):", end=" "); files = input().strip()
    print("🗒️ Additional Notes (optional):", end=" "); notes = input().strip()

    instruction = generate_instruction(
        task_name=task_name,
        task_type=task_type,
        input_desc=input_desc,
        output_desc=output_desc,
        required_files=files,
        notes=notes
    )

    save_instruction_set([instruction], ADMIN_REVIEW_FILE)
    print(f"\n✅ New instruction sent to admin review queue: {ADMIN_REVIEW_FILE}")

# ╔═════════════════════════════╗
# ║ 🧪 CLI: Sample Instruction  ║
# ╚═════════════════════════════╝
@auto_model
@auto_route
@auto_logic
def build_sample():
    build_sample_instruction_set()
    print(f"✅ Sample instructions saved to: {INSTRUCTION_FILE}")

# ╔═════════════════════════════════════╗
# ║ 🔍 CLI: Admin Review Queue Viewer   ║
# ╚═════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
def view_admin_review_queue():
    if not os.path.exists(ADMIN_REVIEW_FILE):
        print("⚠️ No pending instructions for review.")
        return

    with open(ADMIN_REVIEW_FILE, "r", encoding="utf-8") as f:
        instructions = json.load(f)

    if not instructions:
        print("✅ Admin review queue is empty.")
        return

    approved = []
    rejected = []

    print("\n📘 Instruction Editor - Admin Task Review")

    for i, task in enumerate(instructions):
        print(f"\n🔢 {i+1}. {task['task_name']} ({task['task_type']})")
        print(f"📥 Input: {task.get('input_desc', '')}")
        print(f"📤 Output: {task.get('output_desc', '')}")
        print(f"📁 Files: {task.get('files', '')}")
        print(f"📝 Notes: {task.get('notes', '')}")

        while True:
            choice = input("\nWhat do you want to do?\n  [a] Approve\n  [e] Edit Manually\n  [x] Reject\nEnter choice: ").strip().lower()

            if choice == "a":
                approved.append(task)
                print("✅ Approved")
                break
            elif choice == "e":
                new_desc = input("📝 Enter new description:\n> ")
                task["output_desc"] = new_desc
                print("✏️ Updated.")
            elif choice == "x":
                rejected.append(task)
                print("❌ Rejected")
                break
            else:
                print("⚠️ Invalid choice. Try again.")

    with open(FINAL_FILE, "w", encoding="utf-8") as f:
        json.dump(approved, f, indent=2)

    with open(REJECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(rejected, f, indent=2)

    print(f"\n🧾 Review Complete — Approved: {len(approved)}, Rejected: {len(rejected)}")
    print(f"📂 Saved as:\n  ✅ {FINAL_FILE}\n  ❌ {REJECTED_FILE}")

# ╔══════════════════════════╗
# ║ 🚀 Script Entry Point    ║
# ╚══════════════════════════╝
if __name__ == "__main__":
    import json

    print("\n📌 SmartSwasthya Instruction Editor")
    print("────────────────────────────────────────────")
    print("1. Build sample instruction set")
    print("2. Create custom instruction")
    print("3. Admin review queue")

    choice = input("Select option (1/2/3): ").strip()

    if choice == "1":
        build_sample_instruction_set()

    elif choice == "2":
        create_custom_instruction()

    elif choice == "3":
        print("\n📋 Admin Review Queue")
        print("────────────────────────────────────────────")
        try:
            with open(ADMIN_REVIEW_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("❌ admin_review_queue.json not found.")
            exit()

        pending_tasks = [
            task for task in data if "pending" in task.get("status", "").lower()
        ]

        if not pending_tasks:
            print("⚠️ No pending instructions for review.")
        else:
            for idx, task in enumerate(pending_tasks, 1):
                print(f"\n🔹 Task {idx}")
                print(f"📌 Logic Name: {task.get('logic', '[missing]')}")
                print(f"📁 File: {task.get('file', '[missing]')}")
                print(f"📝 Description: {task.get('description', '[missing]')}")
                print(f"🕒 Generated At: {task.get('generated_at', '[missing]')}")
                print(f"📊 Status: {task.get('status', '[missing]')}")

                print("✅ A. Approve\n❌ R. Reject\n➡️ S. Skip to next")
                action = input("Choose (A/R/S): ").strip().lower()

                if action == "a":
                    task["status"] = "✅ Approved"
                elif action == "r":
                    task["status"] = "❌ Rejected"
                elif action == "s":
                    continue
                else:
                    print("⚠️ Invalid choice. Skipping...")

            # Save updated queue
            with open(ADMIN_REVIEW_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("\n💾 Admin review updates saved.")

    else:
        print("❌ Invalid option selected.")

@auto_model
@auto_route
@auto_logic
def edit_instruction(task_id: str, new_instruction: str):
    db = SessionLocal()
    task = db.query(DevTask).filter(DevTask.task_id == task_id).first()
    if task:
        task.description = new_instruction
        task.updated_at = datetime.utcnow()
        db.commit()
        log_instruction_edit(task_id, new_instruction)  # ✅ Log after DB update
    db.close()

