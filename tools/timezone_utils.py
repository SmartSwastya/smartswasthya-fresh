# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

def now_ist():
    return datetime.now(IST)

def utc_to_ist(dt):
    return dt.astimezone(IST)

