# tools/devops/detect_suspicious_code.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import os
import re
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
IGNORE_FOLDERS = {"__pycache__", ".git", ".vscode", ".idea", "records", "node_modules", "static"}

PATTERNS = {
    "exec_eval_compile": r"\b(exec|eval|compile)\s*\(",
    "dangerous_imports": r"\b(import|from)\s+(os|subprocess|pickle|pty|shlex|base64|socket|http|urllib)\b",
    "hardcoded_secrets": r"\b(password|token|key|secret)\s*=\s*[\"'].*?[\"']",
    "wildcard_imports": r"from\s+\S+\s+import\s+\*",
# @auto_flag: encoded_blobs [b64decode]
# ⚠️ Encoded binary/blob found — verify authenticity
# @auto_flag: encoded_blobs [b64decode]
# ⚠️ Encoded binary/blob found — verify authenticity
# @auto_flag: encoded_blobs [b64decode]
# ⚠️ Encoded binary/blob found — verify authenticity
    "encoded_blobs": r"b64decode|zlib\.decompress|\bhex\b|bytes\.fromhex",
    "input_shell": r"\binput\s*\(|os\.system|os\.popen|subprocess\.Popen|pty\.spawn|shlex\.split",
# @auto_flag: dynamic_imports [__import__]
# ⚠️ Dynamic import detected — avoid in core logic
# @auto_flag: dynamic_imports [__import__]
# ⚠️ Dynamic import detected — avoid in core logic
# @auto_flag: dynamic_imports [__import__]
# ⚠️ Dynamic import detected — avoid in core logic
    "dynamic_imports": r"__import__|importlib\.import_module",
# @auto_flag: script_tags [<script\b.*?>.*?</script>]
# ⚠️ HTML script tag used — validate client-side security
# @auto_flag: script_tags [<script\b.*?>.*?</script>]
# ⚠️ HTML script tag used — validate client-side security
# @auto_flag: script_tags [<script\b.*?>.*?</script>]
# ⚠️ HTML script tag used — validate client-side security
    "script_tags": r"<script\b.*?>.*?</script>",
}

def is_text_file(filename):
    return filename.endswith(('.py', '.js', '.sh', '.html', '.env', '.txt', '.json'))

def scan_file(filepath):
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for label, pattern in PATTERNS.items():
                if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
                    matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
                    results.append({
                        "file": filepath,
                        "type": label,
                        "matches": list(set(matches))
                    })
    except Exception as e:
        results.append({
            "file": filepath,
            "type": "error",
            "error": str(e)
        })
    return results

def recursive_scan():
    suspicious = []
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]
        for file in files:
            if is_text_file(file):
                full_path = os.path.join(root, file)
                suspicious.extend(scan_file(full_path))
    return suspicious

def summarize(findings):
    summary = {}
    for item in findings:
        t = item.get("type")
        summary[t] = summary.get(t, 0) + 1
    return summary

if __name__ == "__main__":
    findings = recursive_scan()
    summary = summarize(findings)

    os.makedirs("records", exist_ok=True)
    with open("records/suspicious_code_report.json", "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2)

    print("\nSmart Code Guardian — Suspicious Code Scanner")
    print("--------------------------------------------------")
    print(f"[✔] Total files scanned: {len(set(item['file'] for item in findings))}")
    print(f"[X] Suspicious matches found: {len(findings)}")
    for t, count in summary.items():
        print(f"    → {t} : {count}")
    print(f"\n[→] Full report saved to: records/suspicious_code_report.json\n")
