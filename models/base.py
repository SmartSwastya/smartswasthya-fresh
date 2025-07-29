from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
# models/base.py

from sqlalchemy.orm import declarative_base
import builtins

# Check if Base already defined globally across reloads
if hasattr(builtins, "Base"):
    Base = builtins.Base
else:
    Base = declarative_base()
    builtins.Base = Base


