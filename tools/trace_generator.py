# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# 📁 FILE: tools/trace_generator.py

import os
import re
from datetime import datetime

# --- CONFIGURABLE SECTION ---
TASK_DESCRIPTION_PATH = "logic/instruction_logic.py"  # Where task descriptions are defined
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HANDLER_PATH = os.path.join(PROJECT_ROOT, "handler.py")
DOCKER_FILES = ["Dockerfile", ".dockerignore", "docker-compose.yml"]

TRACE_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "tools", "traces")
os.makedirs(TRACE_OUTPUT_PATH, exist_ok=True)

# --- HELPER FUNCTION ---
@auto_model
@auto_route
@auto_logic
def extract_keywords_from_instruction():
    """Extract task-related keywords from logic/instruction_logic.py"""
    task_keywords = set()
    try:
        with open(os.path.join(PROJECT_ROOT, TASK_DESCRIPTION_PATH), "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(r'task_name\s*=\s*"(.*?)"', line)
                if match:
                    task_keywords.add(match.group(1).strip())
    except Exception as e:
        print("[!] Failed to extract from instruction_logic.py:", e)
    return sorted(task_keywords)


@auto_model
@auto_route
@auto_logic
def trace_keywords_in_handler(keywords):
    """Live scan handler.py for relevant keyword references"""
    traces = {}
    try:
        with open(HANDLER_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for keyword in keywords:
                results = []
                for idx, line in enumerate(lines, 1):
                    if re.search(rf"\\b{re.escape(keyword)}\\b", line, re.IGNORECASE):
                        results.append(f".\\handler.py:{idx}: {line.strip()}")
                if results:
                    traces[keyword] = results
    except Exception as e:
        print("[!] Error reading handler.py:", e)
    return traces


@auto_model
@auto_route
@auto_logic
def check_docker_file_references():
    """Special manual trace access system for core Docker files"""
    core_results = []
    for filename in DOCKER_FILES:
        file_path = os.path.join(PROJECT_ROOT, filename)
        if os.path.exists(file_path):
            core_results.append(f"[AVAILABLE] {filename}")
        else:
            core_results.append(f"[NOT FOUND] {filename}")
    return core_results


@auto_model
@auto_route
@auto_logic
def write_trace_to_txt(traces, core_docker_status):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"trace_dump_{now}.txt"
    full_path = os.path.join(TRACE_OUTPUT_PATH, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        for keyword, lines in traces.items():
            f.write(f"\n➤ trace {keyword}\n")
            for line in lines:
                f.write(line + "\n")
        f.write("\n# --- Core Dockerfile Trace Access ---\n")
        for status in core_docker_status:
            f.write(status + "\n")
    print(f"[✓] Trace saved: {filename}")


# --- MAIN RUNNER ---
if __name__ == "__main__":
    keywords = extract_keywords_from_instruction()
    traces = trace_keywords_in_handler(keywords)
    docker_core_info = check_docker_file_references()
    write_trace_to_txt(traces, docker_core_info)

