import subprocess
import time

def has_changes():
    try:
        output = subprocess.check_output(["git", "status", "--porcelain"])
        return bool(output.strip())
    except:
        return False

while True:
    if has_changes():
        subprocess.run(["git", "add", "."])
        commit_msg = f"Auto update on {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg])
        subprocess.run(["git", "push", "origin", "main"])
        print("Change detected! Committed and pushed.")
    time.sleep(5)  # 5 sec wait