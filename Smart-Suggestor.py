# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# SMART-SUGGESTOR SCRIPT (Python version)
# Location: root/smartswasthya/Smart-Suggestor.py

import os
import json

project_root = os.path.dirname(os.path.abspath(__file__))
suggestion_output = os.path.join(project_root, "smart_suggestions.json")

print("\n📡 Running Smart Suggestor...\n")

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to parse JSON: {path}")
    return []

# Load all traces
json_map = {
    "model_trace":     load_json(os.path.join(project_root, "model_trace.json")),
    "route_trace":     load_json(os.path.join(project_root, "route_trace.json")),
    "logic_trace":     load_json(os.path.join(project_root, "logic_trace.json")),
    "function_trace":  load_json(os.path.join(project_root, "function_trace.json")),
    "template_trace":  load_json(os.path.join(project_root, "template_trace.json")),
    "tag_tracker":     load_json(os.path.join(project_root, "tag_tracker.json")),
    "circuit_trace":   load_json(os.path.join(project_root, "tools", "circuit_trace.json"))
}

def recursive_files(folder, ext):
    result = []
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith(ext):
                result.append(os.path.join(dirpath, f).replace("\\", "/"))
    return result

# Actual files
model_files     = recursive_files(os.path.join(project_root, "models"), ".py")
route_files     = recursive_files(os.path.join(project_root, "routes"), ".py")
logic_files     = recursive_files(os.path.join(project_root, "logic"), ".py")
template_files  = recursive_files(os.path.join(project_root, "templates"), ".html")

def flatten_trace(trace_list, key):
    if not isinstance(trace_list, list):
        return []
    return sorted(list(set(
        item.get(key, "").replace("\\", "/") for item in trace_list if key in item
    )))

model_paths    = flatten_trace(json_map["model_trace"], "file")
route_paths    = flatten_trace(json_map["route_trace"], "file")
logic_paths    = flatten_trace(json_map["logic_trace"], "file")
template_paths = flatten_trace(json_map["template_trace"], "template")

def detect_missing(actual_files, trace_paths, type_name):
    suggestions = []
    for f in actual_files:
        rel = os.path.relpath(f, project_root).replace("\\", "/")
        if rel not in trace_paths:
            suggestions.append({
                "type": type_name,
                "file": rel,
                "suggestion": "Missing in trace"
            })
    return suggestions

# Run checks
model_missing    = detect_missing(model_files, model_paths, "model")
route_missing    = detect_missing(route_files, route_paths, "route")
logic_missing    = detect_missing(logic_files, logic_paths, "logic")
template_missing = detect_missing(template_files, template_paths, "template")

# Merge and output
final_suggestions = model_missing + route_missing + logic_missing + template_missing

with open(suggestion_output, "w", encoding="utf-8") as f:
    json.dump(final_suggestions, f, indent=4)

# Output
print("✅ Suggestions saved to:", suggestion_output)
print("\n🧠 Suggestion types: Missing trace, registration gaps, modularization help\n")
