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
import tarfile
import tempfile
from fastapi import FastAPI, UploadFile, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

extracted_tar_base = tempfile.mkdtemp(prefix="tar_viewer_")
extracted_tar_files = {}
scanned_folder_files = {}
EXCLUDE_DIRS = {"__pycache__", ".git", ".idea", ".vscode"}

# --------------------------------- HTML UI ---------------------------------

HTML_TEMPLATE = """
<!-- @auto_template -->
<!DOCTYPE html>
<html>
<head>
    <title>🕵️ TAR & Folder Viewer</title>
    <style>
        body { background: #121212; color: white; font-family: monospace; display: flex; gap: 2rem; padding: 1rem; }
        .panel { width: 50%; }
        h1 { color: #90ee90; }
        input, select, textarea { width: 100%; margin: 0.4rem 0; padding: 0.4rem; background: #1f1f1f; color: white; border: 1px solid #444; }
        textarea { height: 400px; }
        button { padding: 0.4rem 0.8rem; margin-top: 0.4rem; background: #333; color: white; border: none; cursor: pointer; }
        .copy-btn { float: right; }
    </style>
    <script>
        function openInNotepad() {
            let path = document.getElementById("folderfilelist").value;
            if (!path) {
                alert("⚠️ Please select a file first.");
                return;
            }
            fetch(`/open_notepad?path=${encodeURIComponent(path)}`)
                .then(response => {
                    if (response.ok) {
                        alert("✅ Opened in Notepad.");
                    } else {
                        alert("❌ Failed to open in Notepad.");
                    }
                });
        }
    </script>
    <script>
        let tarFiles = [];
        let folderFiles = [];
        let tarFileContents = {};
        let folderFileContents = {};

        function filterDropdown(inputId, dropdownId, fileList, autoLoadCallback, fileContents) {
            const input = document.getElementById(inputId).value.toLowerCase();
            const dropdown = document.getElementById(dropdownId);
            dropdown.innerHTML = "";

            const filtered = fileList.filter(file => {
                const content = fileContents[file] || "";
                return file.toLowerCase().includes(input) || content.toLowerCase().includes(input);
            });

            filtered.forEach(file => {
                const option = document.createElement("option");
                option.text = file;
                dropdown.add(option);
            });

            if (filtered.length === 1) {
                dropdown.selectedIndex = 0;
                if (typeof autoLoadCallback === 'function') {
                    autoLoadCallback();
                }
            }
        }

        async function uploadTar() {
            let form = new FormData();
            form.append("file", document.getElementById("tarfile").files[0]);
            const res = await fetch("/upload_tar", { method: "POST", body: form });
            const data = await res.json();
            tarFiles = data.files;
            tarFileContents = {};
            for (let file of tarFiles) {
                const res = await fetch(`/read_tar?path=${encodeURIComponent(file)}`);
                const data = await res.json();
                tarFileContents[file] = data.content || "";
            }
            filterDropdown("tarsearch", "tarfilelist", tarFiles, loadTarFile, tarFileContents);
            document.getElementById("tarviewer").value = "";
        }

        async function loadTarFile() {
            let path = document.getElementById("tarfilelist").value;
            const res = await fetch(`/read_tar?path=${encodeURIComponent(path)}`);
            const data = await res.json();
            document.getElementById("tarviewer").value = data.content;
        }

        async function scanFolder() {
            let path = document.getElementById("folderinput").value;
            const res = await fetch(`/scan_folder?path=${encodeURIComponent(path)}`);
            const data = await res.json();
            folderFiles = data.files;
            folderFileContents = {};
            for (let file of folderFiles) {
                const res = await fetch(`/read_folder?path=${encodeURIComponent(file)}`);
                const data = await res.json();
                folderFileContents[file] = data.content || "";
            }
            filterDropdown("foldersearch", "folderfilelist", folderFiles, loadFolderFile, folderFileContents);
            document.getElementById("folderviewer").value = "";
        }

        async function loadFolderFile() {
            let path = document.getElementById("folderfilelist").value;
            const res = await fetch(`/read_folder?path=${encodeURIComponent(path)}`);
            const data = await res.json();
            document.getElementById("folderviewer").value = data.content;
        }

        function copyContent(id) {
            let txt = document.getElementById(id);
            txt.select();
            txt.setSelectionRange(0, 99999);
            document.execCommand("copy");
            alert("Copied!");
        }
    </script>
</head>
<body>

<div class="panel">
    <h1>📦 TAR Viewer</h1>
    <input type="file" id="tarfile" onchange="uploadTar()">
    <input type="text" id="tarsearch" placeholder="Filter files..." onkeyup="filterDropdown('tarsearch', 'tarfilelist', tarFiles, loadTarFile, tarFileContents)">
    <select id="tarfilelist" onchange="loadTarFile()"></select>
    <button class="copy-btn" onclick="copyContent('tarviewer')">📋 Copy</button>
    <textarea id="tarviewer" rows="25" spellcheck="false"></textarea>
</div>

<div class="panel">
    <h1>📁 Folder Viewer</h1>
    <input type="text" id="folderinput" placeholder="Enter full folder path & press Scan">
    <button onclick="scanFolder()">📂 Scan Folder</button>
    <input type="text" id="foldersearch" placeholder="Filter files..." onkeyup="filterDropdown('foldersearch', 'folderfilelist', folderFiles, loadFolderFile, folderFileContents)">
    <select id="folderfilelist" onchange="loadFolderFile()"></select>
    <button class="copy-btn" onclick="copyContent('folderviewer')">📋 Copy</button>
    <button class="copy-btn" onclick="openInNotepad()">📝 Notepad</button>
    <textarea id="folderviewer" rows="25" spellcheck="false"></textarea>
</div>

</body>
</html>
"""

# --------------------------------- Routes ---------------------------------

@app.get("/", response_class=HTMLResponse)
@auto_model
@auto_route
@auto_logic
def ui():
    return HTML_TEMPLATE

@app.post("/upload_tar")
async def upload_tar(file: UploadFile):
    extract_path = tempfile.mkdtemp(dir=extracted_tar_base)
    tar_path = os.path.join(extract_path, file.filename)
    with open(tar_path, "wb") as f:
        f.write(await file.read())
    with tarfile.open(tar_path) as tar:
        tar.extractall(path=extract_path)

    paths = []
    for root, _, files in os.walk(extract_path):
        if any(part in EXCLUDE_DIRS for part in root.split(os.sep)):
            continue
        for name in files:
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, extract_path)
            extracted_tar_files[rel_path] = full_path
            paths.append(rel_path)
    return JSONResponse({"files": sorted(paths)})

@app.get("/read_tar")
@auto_model
@auto_route
@auto_logic
def read_tar(path: str = Query(...)):
    real_path = extracted_tar_files.get(path)
    if not real_path:
        return JSONResponse({"error": "Not found"}, status_code=404)
    with open(real_path, "r", encoding="utf-8", errors="ignore") as f:
        return JSONResponse({"content": f.read()})

@app.get("/scan_folder")
@auto_model
@auto_route
@auto_logic
def scan_folder(path: str = Query(...)):
    if not os.path.isdir(path):
        return JSONResponse({"error": "Invalid path"}, status_code=400)
    folderFiles = {}
    paths = []
    for root, _, files in os.walk(path):
        if any(part in EXCLUDE_DIRS for part in root.split(os.sep)):
            continue
        for name in files:
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, path)
            folderFiles[rel_path] = full_path
            paths.append(rel_path)
    scanned_folder_files.clear()
    scanned_folder_files.update(folderFiles)
    return JSONResponse({"files": sorted(paths)})

@app.get("/read_folder")
@auto_model
@auto_route
@auto_logic
def read_folder(path: str = Query(...)):
    real_path = scanned_folder_files.get(path)
    if not real_path:
        return JSONResponse({"error": "Not found"}, status_code=404)
    with open(real_path, "r", encoding="utf-8", errors="ignore") as f:
        return JSONResponse({"content": f.read()})

@app.get("/open_notepad")
@auto_model
@auto_route
@auto_logic
def open_notepad(path: str = Query(...)):
    # Security: Only allow opening from scanned_folder_files
    if path not in scanned_folder_files:
        return {"error": "Invalid file path"}

    try:
        full_path = os.path.abspath(path)
# @auto_flag: input_shell [subprocess.Popen]
# ⚠️ input() or shell call found — sanitize required
# @auto_flag: input_shell [subprocess.Popen]
# @auto_flag: input_shell [input(]
# ⚠️ input() or shell call found — sanitize required
# ⚠️ input() or shell call found — sanitize required
# @auto_flag: input_shell [subprocess.Popen]
# ⚠️ input() or shell call found — sanitize required
        subprocess.Popen(["notepad", full_path])
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}
# --------------------------------- Run ---------------------------------

if __name__ == "__main__":
    uvicorn.run("tools.devops.inspector:app", host="0.0.0.0", port=8600, reload=True)

