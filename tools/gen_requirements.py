# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# tools/gen_requirements.py
import toml

@auto_model
@auto_route
@auto_logic
def extract_requirements(pyproject_path="pyproject.toml", output_path="requirements.txt"):
    with open(pyproject_path, "r") as f:
        pyproject = toml.load(f)
    
    deps = pyproject.get("project", {}).get("dependencies", [])
    
    with open(output_path, "w") as f:
        for dep in deps:
            f.write(f"{dep}\n")
    
    print(f"✅ requirements.txt generated from {pyproject_path} with {len(deps)} packages.")

if __name__ == "__main__":
    extract_requirements()

