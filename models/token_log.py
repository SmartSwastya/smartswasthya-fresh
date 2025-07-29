from typing import TYPE_CHECKING
# models/token_log.py
from pydantic import BaseModel

class TokenLog(BaseModel):
    token: str
    timestamp: str

