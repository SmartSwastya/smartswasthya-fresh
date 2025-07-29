# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
import os
import json, time, datetime, subprocess, logging
from flask import Flask, request, jsonify, render_template_string
from logging.handlers import RotatingFileHandler
from marker_decorators import auto_logic, auto_route, auto_model

# App Init
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(ROOT_DIR, os.getenv("TEMPLATE_FOLDER", "templates"))
STATIC_DIR = os.path.join(ROOT_DIR, os.getenv("STATIC_FOLDER", "static"))
ROUTE_DIR = "routes"
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Logger Setup
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
logger = logging.getLogger('guardian_logger')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(os.path.join(LOG_DIR, 'guardian.log'), maxBytes=1_000_000, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Constants
EXCLUDE_DIRS = {"__pycache__", ".git", ".idea", ".vscode", "node_modules", ".internal_logs", "correction_logs"}
EXCLUDE_EXTENSIONS = {".csv", ".tar", ".log", ".json", ".bak", ".txt"}
EXCLUDE_FILENAMES = {"handler.log", "safe_paths.json", "project_health.json", "tag_tracker.json"}
COMMAND_HISTORY = []

PROJECT_HEALTH, SAFE_LOG, TAG_TRACKER = "project_health.json", "safe_paths.json", "tag_tracker.json"
CRITICAL_FILES = ["app.py", "input.py", "handler.py"]
STATUS = {
    "mode": "guardian", "port": 5050, "state": "Monitoring",
    "last_checked": str(datetime.datetime.now()), "recovered": True,
    "last_backup": "None", "safe_folders": [], "missing_routes": 0, "missing_files": []
}

STRUCTURE_RULES = {
    "app.py": ["input"], "input.py": ["smartswasthya"],
    "smartuser.py": ["smartuser", "partner", "sections", "family"],
    "sections.py": ["models"]
}

@auto_model
@auto_route
@auto_logic
def is_valid_file(name):
    return not (any(name.endswith(ext) for ext in EXCLUDE_EXTENSIONS) or name in EXCLUDE_FILENAMES)

@auto_model
@auto_route
@auto_logic
def check_router_imports(core_file="core.py"):
    if not os.path.exists(core_file):
        return ["❌ core.py not found."]
    with open(core_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    errors = []
    for line in lines:
        if "include_router" in line and "router" in line:
            try:
                mod = line.split("(")[1].split(")")[0].strip().split(".")[0]
                if mod not in open(core_file, encoding="utf-8").read():
                    errors.append(f"⚠️ Possible missing import for: {mod}")
            except: pass
    return errors or ["✅ All routers seem properly included."]

@auto_model
@auto_route
@auto_logic
def check_main_app_entry():
    issues = []
    for f in ["main.py", "app.py"]:
        if not os.path.exists(f):
            issues.append(f"❌ {f} not found.")
            continue
        content = open(f, encoding="utf-8").read()
        if "FastAPI()" not in content and "Flask(" not in content:
            issues.append(f"⚠️ No app instance found in {f}.")
    return issues or ["✅ Entry files contain valid app instances."]

@auto_model
@auto_route
@auto_logic
def check_structure_consistency():
    errors = []
    for f, imports in STRUCTURE_RULES.items():
        if not os.path.exists(f):
            errors.append(f"❌ Missing file: {f}")
            continue
        content = open(f, "r", encoding="utf-8").read()
        for imp in imports:
            if imp not in content:
                errors.append(f"⚠️ {f} should import {imp}.")
    return errors

@auto_model
@auto_route
@auto_logic
def find_duplicate_routes():
    route_map, dupes = {}, []
    for root, _, files in os.walk(ROUTE_DIR):
        for file in files:
            if file.endswith("_routes.py"):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        if "route(" in line and "'" in line:
                            try:
                                r = line.split("'")[1]
                                if r in route_map:
                                    dupes.append((r, route_map[r], path))
                                else:
                                    route_map[r] = path
                            except: pass
    return dupes

@auto_model
@auto_route
@auto_logic
def log(entry):
    COMMAND_HISTORY.append(entry)
    with open("handler.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | {entry}\n")

@auto_model
@auto_route
@auto_logic
def load_safe():
    return json.load(open(SAFE_LOG, encoding='utf-8')) if os.path.exists(SAFE_LOG) else {"safe_folders": []}

@auto_model
@auto_route
@auto_logic
def save_safe(data): json.dump(data, open(SAFE_LOG, "w", encoding="utf-8"), indent=2)

@auto_model
@auto_route
@auto_logic
def add_safe_folder(folder):
    data = load_safe()
    if folder not in data["safe_folders"]:
        data["safe_folders"].append(folder)
        save_safe(data)
        log(f"🛡️ Safe folder added: {folder}")
    STATUS["safe_folders"] = data["safe_folders"]

@auto_model
@auto_route
@auto_logic
def update_tags():
    tag_map = {}
    for root, _, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith(".html"):
                tags = [line.strip() for line in open(os.path.join(root, file), encoding="utf-8") if "<!--" in line and "-->" in line]
                tag_map[file] = tags
    json.dump(tag_map, open(TAG_TRACKER, "w", encoding="utf-8"), indent=2)

@auto_model
@auto_route
@auto_logic
def full_scan():
    print("Scan started")
    health = {"missing_backends": [], "last_scan": str(datetime.datetime.now())}
    safe_paths = load_safe().get("safe_folders", [])
    for f in os.listdir(TEMPLATE_DIR):
        if f.endswith(".html"):
            full_path = f"templates/{f}"
            if full_path not in safe_paths:
                backend = f"{ROUTE_DIR}/{f.replace('.html','')}_routes.py"
                if not os.path.exists(backend):
                    health["missing_backends"].append(f)
    json.dump(health, open(PROJECT_HEALTH, "w", encoding="utf-8"), indent=2)
    STATUS["missing_routes"] = len(health["missing_backends"])
    STATUS["missing_files"] = [f for f in health["missing_backends"] if f"templates/{f}" not in safe_paths]
    log(f"🔍 Scan: {STATUS['missing_routes']} routes missing")

@auto_model
@auto_route
@auto_logic
def trigger_reload(path=None):
    global last_reload
    now = time.time()
    if now - last_reload > 2 and os.path.exists("app.py"):
        os.utime("app.py", None)
        last_reload = now
        log(f"♻️ Reloaded due to: {path}")
last_reload = 0

@auto_model
@auto_route
@auto_logic
def generate_assist(file_name):
    print(f"File {file_name} has been modified.")
    update_tags()
    log(f"File {file_name} processed after modification.")
# =============================================================
# 🌐 Smart Guardian Console — Web Interface + Commands
# =============================================================

HTML_TEMPLATE = """
<!-- @auto_template -->
<!DOCTYPE html>
<html>
<head>
    <title>Smart Console</title>
    <style>
        body {
            margin: 0;
            background: #1e1e2e;
            color: #fff;
            font-family: monospace;
        }
        .header {
            padding: 1rem;
            font-size: 1.5rem;
            background: #313244;
            color: #89dceb;
        }
        .strip {
            padding: 0.5rem;
            background: #2a2a3d;
            border-bottom: 1px solid #444;
            cursor: pointer;
        }
        .arrow::before {
            content: "▶";
            display: inline-block;
            margin-right: 10px;
            transition: transform 0.2s ease;
        }
        .arrow.expanded::before {
            transform: rotate(90deg);
        }
        .content {
            display: none;
            padding: 0.5rem 1.5rem;
            background: #1b1e2e;
            border-left: 3px solid #89dceb;
        }
        .console {
            padding: 1rem;
            background: #181825;
            display: flex;
            gap: 1rem;
        }
        input[type=text] {
            flex: 1;
            padding: 0.5rem;
            background: #313244;
            color: #fff;
            border: none;
        }
        input[type=submit] {
            padding: 0.5rem 1rem;
            background: #89dceb;
            color: #000;
            border: none;
            cursor: pointer;
        }
        .output {
            padding: 1rem;
            white-space: pre-wrap;
            max-height: 40vh;
            overflow: auto;
            border-top: 2px solid #f38ba8;
        }
        .status {
            padding: 0.8rem;
            background: #222;
            color: #b4befe;
            border-top: 1px solid #444;
            font-size: 0.9rem;
        }
        .content span {
            display: block;
            margin-bottom: 20px;
            padding: 5px 10px;
            background-color: #2c3e50;
            color: white;
            border-radius: 5px;
        }
    </style>

    <script>
        function fill(cmd) { document.querySelector("input[name='cmd']").value = cmd; }
        function run(cmd) { 
            fetch("/command", {
                method: "POST",
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: "cmd=" + encodeURIComponent(cmd)
            }).then(() => location.reload());
        }
        document.addEventListener("DOMContentLoaded", function () {
            document.querySelectorAll(".arrow").forEach(function (el) {
                el.addEventListener("click", function () {
                    el.classList.toggle("expanded");
                    let next = el.nextElementSibling;
                    next.style.display = next.style.display === "block" ? "none" : "block";
                });
            });
        });
        function showHealthDetails() { document.getElementById("healthDetailBox").style.display = "block"; }
        function hideHealthDetails() { document.getElementById("healthDetailBox").style.display = "none"; }
    </script>
</head>
<body>
    <div class="header">🛡️ Smart Guardian Console — v12.7</div>

    <div class="strip arrow">▶ Scan Results</div>
    <div class="content">✅ Project scanned<br>⚠️ {{ status["missing_routes"] }} route(s) missing<br></div>

    <div class="strip arrow">▶ Suggestions</div>
    <div class="content">
        {% for m in status.get("missing_files", []) %}
            💡 Create {{ m.replace('.html', '_routes.py') }} for {{ m }}<br>
        {% endfor %}
    </div>

    <div class="strip arrow">▶ Commands</div>
    <div class="content">
        <span onclick="run('scan')">Run Full Scan</span><br>
        <span onclick="run('tags')">Update Tags</span><br>
        <span onclick="run('check_structure')">Check Project Structure</span><br>
        <span onclick="run('safe templates')">Mark templates/ as Safe</span><br>
        <span onclick="run('map')">📂 Project Structure</span><br>
        <span onclick="run('duplicate_routes')">Find Duplicate Routes</span><br>  
        <span onclick="run('reload')">Trigger Server Reload</span><br>  
        <span onclick="run('generate_assist')">Generate Assist (After File Modification)</span><br>  
        <span onclick="run('log')">View Logs</span><br>
    </div>

    <div class="strip arrow">▶ Quick Fill</div>
    <div class="content">
        <span onclick="fill('search *replace_here')">search</span><br>
        <span onclick="fill('trace *replace_here')">trace</span><br>
        <span onclick="fill('map *replace_here')">map</span><br>
        <span onclick="fill('restore *replace_here')">restore</span><br>
        <span onclick="fill('add_blueprint *replace_here')">add_blueprint</span><br>
        <span onclick="fill('add_route *file *route GET')">add_route</span><br>
        <span onclick="fill('rename_route *old *new')">rename_route</span><br>
    </div>

    <div class="output">
        {% for i in history %}
            <div>➤ <b>{{ i.split('\\n')[0] }}</b><br>{{ i.split('\\n', 1)[1] if '\\n' in i else '' }}</div><br>
        {% endfor %}
    </div>

    <form method="POST" action="/command" class="console">
        <input type="text" name="cmd" placeholder="Type command..." autofocus autocomplete="off">
        <input type="submit" value="Run">
    </form>

    <div class="status" onmouseover="showHealthDetails()" onmouseout="hideHealthDetails()">
        🩺 Health: {{ status["missing_routes"] }} missing | 🛡️ Safe: {{ status["safe_folders"]|length }} folders | 💾 Last Backup: {{ status["last_backup"] }}
        <div id="healthDetailBox" style="display:none;background:#1b1e2e;padding:0.6rem;margin-top:0.4rem;border-top:1px solid #f38ba8;">
            {% for m in status.get("missing_files", []) %}
                • {{ m }}<br>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
@auto_model
@auto_route
@auto_logic
def home():
    STATUS["last_checked"] = str(datetime.datetime.now())
    return render_template_string(HTML_TEMPLATE, history=COMMAND_HISTORY[-20:], status=STATUS)

@auto_model
@auto_route
@auto_logic
def rename_route(old, new):
    for root, _, files in os.walk(ROUTE_DIR):
        for file in files:
            if file.endswith("_routes.py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                updated, changed = [], False
                for line in lines:
                    if f"@".lower() in line.lower() and f"route('{old}'" in line:
                        updated.append(line.replace(f"'{old}'", f"'{new}'"))
                        changed = True
                    else:
                        updated.append(line)
                if changed:
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(updated)
                    return f"✅ Route renamed: {old} ➜ {new} in {file}"
    return f"❌ Route '{old}' not found in any route file."

@app.route("/command", methods=["POST"])
@auto_model
@auto_route
@auto_logic
def command():
    cmd = request.form.get("cmd", "").strip()
    out = "❌ Unknown command."

    if cmd == "scan":
        full_scan()
        out = "✅ Project scanned."
    elif cmd == "tags":
        update_tags()
        out = "✅ Tags updated."
    elif cmd == "check_structure":
        result = check_structure_consistency()
        out = "\n".join(result or ["✅ Structure is perfectly aligned!"])
    elif cmd == "duplicate_routes":
        duplicates = find_duplicate_routes()
        out = "\n".join([f"Duplicate route: {route}" for route in duplicates]) or "✅ No duplicate routes found."
    elif cmd == "reload":
        trigger_reload(None)
        out = "✅ Server reloaded."
    elif cmd == "generate_assist":
        generate_assist("modified_file")
        out = "✅ Assist generated for modified file."
    elif cmd == "log":
        with open("handler.log", "r", encoding="utf-8") as f:
            log_content = f.read()
        out = f"Logs:\n{log_content[:500]}"
    elif cmd.startswith("safe "):
        folder = cmd[5:].strip()
        if os.path.exists(folder):
            add_safe_folder(folder)
            out = f"✅ Marked safe: {folder}"
        else:
            out = f"❌ Not found: {folder}"
    elif cmd == "map":
        out = "📂 Project Structure:\n"
        out += "root/smartswasthya/\n├── app.py\n├── input.py\n├── templates/\n"
        for file in os.listdir(TEMPLATE_DIR):
            if file.endswith(".html"):
                route = file.replace("_dashboard.html", "").replace(".html", "")
                clean = "/" if route == "index" else f"/{route}"
                out += f"│   ├── {file} ➝ {clean}\n"
        out += "├── routes/\n"
        for file in os.listdir(ROUTE_DIR):
            if file.endswith("_routes.py"):
                out += f"│   ├── {file}\n"
    elif cmd.startswith("map "):
        keyword = cmd.replace("map", "", 1).strip().lower()
        results = []
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if is_valid_file(file) or file in ("Dockerfile", ".env"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, encoding="utf-8") as f:
                            content = f.read().lower()
                            if keyword in content:
                                results.append(f"{filepath}")
                    except:
                        pass
        out = "\n".join([f"🔗 {r}" for r in results]) if results else f"❌ No files found containing '{keyword}'"
    elif cmd.startswith("add_blueprint "):
        name = cmd.split()[1]
        path = f"{ROUTE_DIR}/{name}_routes.py"
        if not os.path.exists(path):
            os.makedirs(ROUTE_DIR, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"from flask import Blueprint, render_template\n{name}_blueprint = Blueprint('{name}', __name__)\n")
            out = f"✅ Created: {name}_routes.py"
        else:
            out = f"⚠️ Already exists: {path}"
    elif cmd.startswith("add_route "):
        parts = cmd.split()
        if len(parts) == 4:
            file, route, method = parts[1], parts[2], parts[3].upper()
            path = f"{ROUTE_DIR}/{file}_routes.py"
            func = f"\n@{file}_blueprint.route('{route}', methods=['{method}'])\ndef {file}_page():\n    return render_template('{file}.html')\n"
            with open(path, "a", encoding="utf-8") as f:
                f.write(func)
            out = f"✅ Route added to {path}"
        else:
            out = "❌ Usage: add_route file /path METHOD"
    elif cmd.startswith("rename_route "):
        parts = cmd.split()
        if len(parts) == 3:
            old, new = parts[1], parts[2]
            out = rename_route(old, new)
        else:
            out = "❌ Usage: rename_route /old /new"
    elif cmd.startswith("trace "):
        keyword = cmd.split(" ", 1)[1]
        matches = []
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if is_valid_file(file) or file in ("Dockerfile", ".env"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            for i, line in enumerate(f):
                                if keyword in line:
                                    matches.append(f"{path}:{i + 1}: {line.strip()}")
                    except:
                        continue
        out = "\n".join(matches) or f"❌ No trace found for '{keyword}'"
    elif cmd.startswith("search "):
        terms = cmd[7:].split()
        result = []
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if is_valid_file(file) or file in ("Dockerfile", ".env"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            for i, line in enumerate(f):
                                if any(t in line for t in terms):
                                    result.append(f"{path}:{i+1}: {line.strip()}")
                    except:
                        pass
        out = "\n".join(result[:50]) or "❌ No match."
    elif cmd == "errors":
        try:
            with open("handler.log", "r", encoding="utf-8") as f:
                lines = f.readlines()
            error_lines = [l.strip() for l in lines if any(k in l for k in ["Exception", "Error", "Traceback"])]
            if not error_lines:
                out = "✅ No errors logged."
            else:
                recent = error_lines[-5:]
                suggestions = []
                for l in recent:
                    parts = l.split("|", 1)
                    msg = parts[1].strip() if len(parts) > 1 else l
                    key = msg.split()[0]
                    suggestions.append(f"trace {key}")
                out = "Errors:\n" + "\n".join(recent) + "\n\nSuggestions:\n" + "\n".join(suggestions)
        except Exception as e:
            out = f"❌ Could not read error log: {e}"
    else:
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            out = e.output

    log(f"{cmd}\n{out}")
    return home()

# handler.py (safe fallback marker for legacy compatibility)
@auto_model
@auto_route
@auto_logic
def auto_logic(func): return func
@auto_model
@auto_route
@auto_logic
def auto_route(func): return func
@auto_model
@auto_route
@auto_logic
def auto_model(cls): return cls

# =============================================================
# 🏁 Start App
# =============================================================
if __name__ == "__main__":
    full_scan()
    update_tags()
    app.run(host="0.0.0.0", port=5050, debug=True, use_reloader=False)
