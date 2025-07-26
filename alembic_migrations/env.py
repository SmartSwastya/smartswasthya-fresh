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
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from models import models

# ==========================================
# ✅ STANDARDIZED BASE PATH SETUP
# ==========================================
PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ==========================================
# ✅ DATABASE MODELS IMPORTS
# ==========================================
from models import models  # must load Base + all models internally
from models.base import Base

# Force-import specific Alembic trackable models
import models.task_tracker.task_master
import models.task_tracker.code_snippet_map
import models.task_tracker.model_trace
import models.task_tracker.route_trace
import models.task_tracker.task_status_history
import models.task_tracker.dev_assignment_log

# ==========================================
# ✅ ALEMBIC CONFIGURATION
# ==========================================
config = context.config
fileConfig(config.config_file_name)

config.set_main_option(
    'sqlalchemy.url',
    os.getenv('DATABASE_URL', 'postgresql://postgres:newpassword@smart_db:5432/smartswasthya')
)

target_metadata = Base.metadata

# ==========================================
# ✅ OFFLINE MIGRATION RUNNER
# ==========================================
@auto_model
@auto_route
@auto_logic
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# ==========================================
# ✅ ONLINE MIGRATION RUNNER
# ==========================================
@auto_model
@auto_route
@auto_logic
def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # detect column type changes
        )
        with context.begin_transaction():
            context.run_migrations()

# ==========================================
# ✅ EXECUTION MODE DECIDER
# ==========================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
