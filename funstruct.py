import os
import json
import re
from collections import defaultdict, deque

# Load actual trackedlist.txt
TRACKED_FILE = 'trackedlist.txt'  # Current dir मध्ये assume
try:
    with open(TRACKED_FILE, 'r', encoding='utf-8') as f:
        tracked_content = f.read()
except FileNotFoundError:
    tracked_content = ""  # Fallback if missing
    print("⚠️ trackedlist.txt not found; using empty.")

# Trace function (as before)
EXCLUDE_DIRS = ['__pycache__', '.git', 'venv']
def trace_keyword(keyword, project_root='.'):
    matches = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(('.py', '.html', '.js', '.txt')) or file in ("Dockerfile", ".env"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f):
                            if re.search(rf'\b{re.escape(keyword)}\b', line, re.IGNORECASE):
                                matches.append(f"{path}:{i + 1}: {line.strip()}")
                except:
                    continue
    return matches or [f"❌ No trace found for '{keyword}'"]

# Generator
def generate_funstruct(start_keyword='fastapi', max_depth=5):
    structure = defaultdict(list)
    conflicts = []
    
    # Parse categories
    lines = tracked_content.strip().split('\n')
    for file_path in lines:
        parts = file_path.split('/')
        category = parts[0] if len(parts) > 1 else 'root'
        structure[category].append(file_path)
    
    # BFS Tracing with path tracking
    traced = set()
    tree = {}
    queue = deque([(start_keyword, [])])  # (kw, path_to_parent)
    
    while queue and max_depth > 0:
        kw, path = queue.popleft()
        if kw in traced:
            conflicts.append(f"⚠️ Circular dependency suspected for '{kw}'")
            continue
        traced.add(kw)
        
        matches = trace_keyword(kw)
        connected_kws = set()
        for match in matches:
            # Improved extraction
            words = re.findall(r'\b(?:from\s+)?(\w+)(?:\s+import)?\b', match.split(':')[-1])
            for word in words:
                if word.lower() not in ['from', 'import', ''] and word in ['routes', 'FastAPI', 'app', 'router', 'tree', 'parent']:  # Expanded rules
                    connected_kws.add(word)
        
        # Remove self-reference
        connected_kws.discard(kw)
        
        # Build nested tree
        node = tree
        for p in path:
            node = node[p]
        node[kw] = {}
        
        # Add children to queue
        for conn in connected_kws:
            if conn not in traced:
                queue.append((conn, path + [kw]))
        
        # Conflicts
        if len(matches) > 50:
            conflicts.append(f"⚠️ High occurrences for '{kw}' - possible duplicate code")
        if len(connected_kws) == 0 and kw != start_keyword:
            conflicts.append(f"⚠️ Broken link for '{kw}' - no connections found")
        
        max_depth -= 1
    
    output = {
        "categories": dict(structure),
        "dependency_tree": tree,
        "conflicts": conflicts
    }
    return json.dumps(output, indent=2)

# Run
print(generate_funstruct())