# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# tools/smart_logger.py

import os
import sys
import datetime

from handler import auto_logic, auto_route, auto_model

# ==== 🔈 Global Debug Toggle ====
TRACE_DEBUG = False

# ==== 🛠 UTF-8 Console Fix ====
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==== 🧠 SmartLogger Class ====
class SmartLogger:
    @auto_model
    @auto_route
    @auto_logic
    def __init__(self, subsystem: str):
        self.subsystem = subsystem
        self.logs = {}

    @auto_model
    @auto_route
    @auto_logic
    def _log(self, level: str, area: str, target: str, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] [{self.subsystem}] [{level}] {area} → {target} :: {message}"
        if TRACE_DEBUG:
            print(formatted)

    @auto_model
    @auto_route
    @auto_logic
    def log(self, message: str, tag: str = "ℹ️ INFO", area: str = "injector", target: str = "-"):
        self._log(tag, area, target, message)

    @auto_model
    @auto_route
    @auto_logic
    def log_success(self, area: str, target: str, message: str):
        self._log("✅ SUCCESS", area, target, message)

    @auto_model
    @auto_route
    @auto_logic
    def log_info(self, area: str, target: str, message: str):
        self._log("ℹ️ INFO", area, target, message)

    @auto_model
    @auto_route
    @auto_logic
    def log_warning(self, area: str, target: str, message: str):
        self._log("⚠️ WARNING", area, target, message)

    @auto_model
    @auto_route
    @auto_logic
    def log_error(self, area: str, target: str, message: str):
        self._log("❌ ERROR", area, target, message)

    @auto_model
    @auto_route
    @auto_logic
    def log_failure(self, area: str, target: str, message: str):
        self._log("❌ FAILURE", area, target, message)

    @auto_model
    @auto_route
    @auto_logic
    def log_note(self, title: str, message: str):
        if TRACE_DEBUG:
            print(f"[📝 NOTE] {title}: {message}")
        if title not in self.logs:
            self.logs[title] = []
        self.logs[title].append({
            "level": "NOTE",
            "area": title,
            "subject": "-",
            "message": message
        })

    @auto_model
    @auto_route
    @auto_logic
    def log_summary(self, title: str):
        self._log("📦 SUMMARY", title, "-", f"Summary block for {title}")

    @auto_model
    @auto_route
    @auto_logic
    def summarize(self, subsystem: str) -> str:
        entries = self.logs.get(subsystem, [])
        summary_lines = [
            f"[{entry['level']}] {entry['area']} → {entry['subject']} :: {entry['message']}"
            for entry in entries
        ]
        return "\n".join(summary_lines) if summary_lines else f"No logs recorded for '{subsystem}'"

# ==== 🚀 Default Logger Instance ====
logger = SmartLogger("Default")
