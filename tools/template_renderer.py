# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# tools/template_renderer.py
from fastapi.responses import HTMLResponse

def render_template(template_name: str, context: dict = {}) -> HTMLResponse:
    # Dummy return for now
    return HTMLResponse(f"<html><body><h1>{template_name}</h1></body></html>")
