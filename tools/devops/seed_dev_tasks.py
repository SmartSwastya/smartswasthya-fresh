# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# tools/devops/seed_dev_tasks.py

import os
import pandas as pd
from sqlalchemy.orm import Session
from models.dev_tasks import DevTask
from database import engine
from sqlalchemy.exc import IntegrityError

csv_path = "tools/devops/input_tasks.csv"
df = pd.read_csv(csv_path)

@auto_model
@auto_route
@auto_logic
def safe_float(val):
    try:
        return float(val)
    except:
        return 0.0

df["logic_score"] = df["logic_score"].apply(safe_float)

session = Session(bind=engine)

print(f"🚀 Seeding {len(df)} tasks into dev_tasks table...")

inserted, skipped = 0, 0

for _, row in df.iterrows():
    try:
        task = DevTask(
            task_id=row["task_id"],
            title=row["title"],
            description=row["description"],
            source_file=row["source_file"],
            mapped_file=row["mapped_file"] if pd.notna(row["mapped_file"]) else None,
            logic_score=row["logic_score"],
            status=row["status"],
            assigned_to=row.get("assigned_to", "unassigned"),
            admin_remarks=row.get("admin_remarks", ""),
            module_group=row.get("Module Group", "")  # ✅ NEW FIELD HERE
        )
        session.add(task)
        inserted += 1
    except IntegrityError:
        session.rollback()
        skipped += 1
        continue
    except Exception as e:
        print(f"❌ Error on task {row.get('task_id', '?')}: {str(e)}")
        session.rollback()

session.commit()
session.close()

print(f"✅ Seeding complete: {inserted} inserted, {skipped} skipped.")

