# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import os
import json
import re

@auto_model
@auto_route
@auto_logic
def build_reverse_trace(whl_dir="tmp/python_packages", out_json="tools/devops/installed_manifest.json"):
    mapping = {}
    for file in os.listdir(whl_dir):
        if file.endswith(".whl"):
            base = file.split("-")[0].lower()
            version = re.findall(r"-([\d\.]+)-", file)
            if version:
                mapping[file] = f"{base}=={version[0]}"
    with open(out_json, "w") as f:
        json.dump(mapping, f, indent=4)
    print(f"✅ Reverse trace written to {out_json}")

if __name__ == "__main__":
    build_reverse_trace()

