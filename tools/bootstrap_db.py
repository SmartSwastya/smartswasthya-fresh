# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from database import engine
from models import Base

print("🔁 Creating all tables from Base.metadata...")
Base.metadata.create_all(bind=engine)
print("✅ Done.")

