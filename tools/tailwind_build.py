# tools/tailwind_build.py
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import subprocess
import os

os.makedirs("static/css", exist_ok=True)

print("📦 Running Tailwind build...")
subprocess.run(
    ['./tailwindcss.exe',
     '-i', 'static/css/input.css',
     '-o', 'static/css/output.css',
     '--config', 'tailwind.config.js',
     '--postcss'],
    check=True
)
print("✅ Tailwind CSS build complete: static/css/output.css")

