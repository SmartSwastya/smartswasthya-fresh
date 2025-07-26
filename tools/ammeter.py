# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import os
import datetime
import json
from collections import defaultdict
from tools.devops.generate_circuit_trace import build_circuit_trace

BASE_DIR = os.path.abspath(os.path.dirname(__file__))              # tools/
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))        # root/smartswasthya
LOG_DIR = os.path.join(PROJECT_DIR, "records", "ammeter_logs")
os.makedirs(LOG_DIR, exist_ok=True)

class Ammeter:
    def __init__(self):
        self.graph = defaultdict(set)
        self.reverse_graph = defaultdict(set)

        print("⚙️ Running live trace generators...")
        circuit = build_circuit_trace()
        for entry in circuit:
            src = entry.get("source")
            dst = entry.get("target")
            if src and dst:
                self.graph[src].add(dst)
                self.reverse_graph[dst].add(src)

    def trace_all_paths(self):
        visited = set()
        broken, partial, complete = [], [], []

        for start in self.graph:
            if start in visited:
                continue
            path = [start]
            visited.add(start)
            current = start
            while current in self.graph and self.graph[current]:
                next_nodes = list(self.graph[current])
                if len(next_nodes) > 1:
                    partial.append((path.copy(), "Multiple targets"))
                    break
                next_node = next_nodes[0]
                if next_node in path:
                    broken.append((path.copy(), "Cycle detected"))
                    break
                path.append(next_node)
                visited.add(next_node)
                current = next_node
            else:
                if len(path) == 1:
                    broken.append((path, "Dead-end"))
                else:
                    complete.append(path)

        return broken, partial, complete

    def get_summary_data(self, broken, partial, complete):
        total = len(broken) + len(partial) + len(complete)
        return {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_paths": total,
            "broken_count": len(broken),
            "partial_count": len(partial),
            "complete_count": len(complete),
            "broken_paths": [{"path": p, "reason": r} for p, r in broken],
            "partial_paths": [{"path": p, "hint": r} for p, r in partial],
            "complete_paths": complete,
        }

    def print_summary(self, broken, partial, complete):
        data = self.get_summary_data(broken, partial, complete)

        print("\n🧠 Ammeter Trace Summary")
        print("─────────────────────────────")
        print(f"➤ Total Paths        : {data['total_paths']}")
        print(f"➤ Broken Paths       : {data['broken_count']}")
        print(f"➤ Partial Paths      : {data['partial_count']}")
        print(f"➤ Complete Circuits  : {data['complete_count']}")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        log_path_txt = os.path.join(LOG_DIR, f"{timestamp}_report.log")
        log_path_json = os.path.join(LOG_DIR, f"{timestamp}_report.json")

        with open(log_path_txt, "w", encoding="utf-8") as logf:
            logf.write("Ammeter Diagnostic Log\n")
            logf.write("=======================\n")
            logf.write(f"Timestamp: {data['timestamp']}\n\n")
            logf.write(f"Total Paths: {data['total_paths']}\n")
            logf.write(f"Broken Paths: {data['broken_count']}\n")
            logf.write(f"Partial Paths: {data['partial_count']}\n")
            logf.write(f"Complete Circuits: {data['complete_count']}\n\n")

            if data['broken_paths']:
                logf.write("Broken Paths:\n")
                for item in data['broken_paths']:
                    logf.write(f"- {' → '.join(item['path'])} [Reason: {item['reason']}]\n")
                logf.write("\n")

            if data['partial_paths']:
                logf.write("Partial Paths:\n")
                for item in data['partial_paths']:
                    logf.write(f"- {' → '.join(item['path'])} [Hint: {item['hint']}]\n")
                logf.write("\n")

            if data['complete_paths']:
                logf.write("Complete Circuits:\n")
                for path in data['complete_paths']:
                    logf.write(f"- {' → '.join(path)}\n")

        with open(log_path_json, "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=2)

        print(f"\n📄 Log saved: {log_path_txt}")
        print(f"📁 JSON saved: {log_path_json}\n")


if __name__ == "__main__":
    print("🔍 Starting Ammeter Diagnostic Pass...")
    ammeter = Ammeter()
    broken, partial, complete = ammeter.trace_all_paths()
    ammeter.print_summary(broken, partial, complete)
