# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# odil/utils.py

import json

@auto_model
@auto_route
@auto_logic
def load_json_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

