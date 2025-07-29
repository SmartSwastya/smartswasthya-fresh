from typing import TYPE_CHECKING
from pydantic import BaseModel

class RestoreBackupRequest(BaseModel):
    file_name: str

