from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import tarfile, zipfile
import tempfile
import shutil
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

scanned_folder_files = {}
EXCLUDE_DIRS = {"__pycache__", ".git", ".idea", ".vscode", ".internal_logs", "node_modules"}
EXCLUDE_EXTS = {".log", ".png", ".csv", ".txt"}

# ------------------------------- HTML UI -------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>📁 Folder Explorer</title>
  <meta charset="UTF-8">
  <style>
    body {
      background: #121212;
      color: white;
      font-family: monospace;
      padding: 1rem;
    }
    h1 {
      color: #90ee90;
    }
    input, button {
      padding: 0.5rem;
      margin: 0.3rem 0;
      background: #1f1f1f;
      color: white;
      border: 1px solid #444;
      width: 100%;
    }
    #fileExplorer {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      padding-top: 1rem;
      border-top: 1px solid #333;
    }
    .file-item {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #2b2b2b;
      border: 1px solid #555;
      padding: 0.4rem 0.6rem;
      border-radius: 5px;
      cursor: grab;
      color: white;
      text-decoration: none;
    }
    .file-item:hover {
      background: #444;
    }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>
  <script>
    let folderFiles = {};
    let selectedFiles = new Set();

    function updateExplorer(filter = "") {
      const explorer = document.getElementById("fileExplorer");
      explorer.innerHTML = "";

      const lower = filter.toLowerCase();
      Object.keys(folderFiles).forEach(path => {
        const content = folderFiles[path];
        if (path.toLowerCase().includes(lower) || content.toLowerCase().includes(lower)) {
          const wrapper = document.createElement("div");
          wrapper.style.display = "flex";
          wrapper.style.alignItems = "center";
          wrapper.style.gap = "5px";

          const checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkbox.checked = selectedFiles.has(path);
          checkbox.onchange = () => {
            if (checkbox.checked) selectedFiles.add(path);
            else selectedFiles.delete(path);
          };

          const contentBlob = new Blob([content], { type: "text/plain" });
          const link = document.createElement("a");
          link.href = URL.createObjectURL(contentBlob);
          link.download = path.split("/").pop();
          link.innerText = path.split("/").pop();
          link.className = "file-item";

          wrapper.appendChild(checkbox);
          wrapper.appendChild(link);
          explorer.appendChild(wrapper);
        }
      });

      // Mount ZIP button if not already present
      let zipBtn = document.getElementById("zipExportBtn");
      if (!zipBtn) {
        zipBtn = document.createElement("button");
        zipBtn.id = "zipExportBtn";
        zipBtn.innerText = "📦 Create ZIP";
        zipBtn.style.marginTop = "1rem";
        zipBtn.style.background = "#222";
        zipBtn.style.color = "#90ee90";
        zipBtn.onclick = downloadZip;
        document.body.appendChild(zipBtn);
      }
    }

    async function scanFolder() {
      const path = document.getElementById("folderinput").value;
      const res = await fetch(`/scan_folder?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      folderFiles = {};
      selectedFiles = new Set();
      if (data.files && data.contents) {
        for (let i = 0; i < data.files.length; i++) {
          const path = data.files[i];
          folderFiles[path] = data.contents[i];
          folderFiles[path + "_realpath"] = data.realpaths[i];
        }
      }
      updateExplorer(document.getElementById("foldersearch").value);
    }

    async function downloadZip() {
      if (selectedFiles.size === 0) return alert("No files selected.");
      const zip = new JSZip();
      selectedFiles.forEach(path => {
        zip.file(path.split("/").pop(), folderFiles[path]);
      });

      const blob = await zip.generateAsync({ type: "blob" });
      const a = document.createElement("a");
      const query = document.getElementById("foldersearch").value.trim() || "download";
      a.href = URL.createObjectURL(blob);
      a.download = `${query}.zip`;
      a.click();
    }
  </script>
</head>
<body>
  <h1>📁 Folder Explorer</h1>
  <input type="text" id="folderinput" placeholder="Enter any folder or archive path (zip/tar)">
  <button onclick="scanFolder()">📂 Scan Folder</button>
  <input type="text" id="foldersearch" placeholder="Filter files..." onkeyup="updateExplorer(this.value)">
  <div id="fileExplorer"></div>
</body>
</html>
"""

# ------------------------------- Folder Scanner -------------------------------

@app.get("/", response_class=HTMLResponse)
def ui():
    return HTML_TEMPLATE

@app.get("/scan_folder")
def scan_folder(path: str = Query(...)):
    if not os.path.exists(path):
        return JSONResponse({"error": "Path does not exist"}, status_code=400)

    if os.path.isdir(path):
        pass
    elif zipfile.is_zipfile(path):
        extract_path = tempfile.mkdtemp(prefix="zip_extract_")
        with zipfile.ZipFile(path, 'r') as z:
            z.extractall(extract_path)
        path = extract_path
    elif tarfile.is_tarfile(path):
        extract_path = tempfile.mkdtemp(prefix="tar_extract_")
        with tarfile.open(path) as tar:
            tar.extractall(path=extract_path)
        path = extract_path
    else:
        return JSONResponse({"error": "Not a valid folder or archive"}, status_code=400)

    paths, contents, realpaths = [], [], []
    for root, _, files in os.walk(path):
        if any(part in EXCLUDE_DIRS for part in root.split(os.sep)):
            continue
        for name in files:
            if os.path.splitext(name)[1] in EXCLUDE_EXTS:
                continue
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, path)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                content = ""
            paths.append(rel_path)
            contents.append(content)
            realpaths.append("file:///" + full_path.replace("\\", "/"))

    return JSONResponse({
        "files": paths,
        "contents": contents,
        "realpaths": realpaths
    })

@app.post("/zip_selected")
def zip_selected(data: dict):
    filenames = data.get("filenames", [])
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "selected.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        for name in filenames:
            full_path = scanned_folder_files.get(name)
            if full_path and os.path.exists(full_path):
                z.write(full_path, arcname=os.path.basename(full_path))
    return FileResponse(zip_path, media_type="application/zip")

# ------------------------------- Run -------------------------------

if __name__ == "__main__":
    uvicorn.run("inspector_v2:app", host="0.0.0.0", port=8600, reload=True)