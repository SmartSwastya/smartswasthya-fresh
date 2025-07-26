# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# tools/smart_template.py

from fastapi.templating import Jinja2Templates
from jinja2 import pass_context
from fastapi import Request
from typing import Optional
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from tools.auth import get_current_user_optional

templates = Jinja2Templates(directory="templates")

@pass_context
def url_for(ctx, name, **params):
    request = ctx.get("request")
    if request:
        try:
            return request.url_for(name, **params)
        except Exception:
            pass
    # fallback — direct path build
    if name == "static" and "filename" in params:
        return f"/static/{params['filename']}"
    return "/404"

# Inject into global context
@pass_context
def current_user(ctx) -> Optional[dict]:
    try:
        request: Request = ctx.get("request")
        user = request.scope.get("user")
        if not user:
            user = request.session.get("user")  # fallback if stored in session
        return user
    except:
        return None

templates.env.globals["url_for"] = url_for
templates.env.globals["current_user"] = current_user
templates.env.globals['now'] = datetime.now
