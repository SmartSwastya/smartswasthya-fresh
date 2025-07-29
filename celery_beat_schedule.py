# celery_beat_schedule.py
from celery.schedules import crontab

beat_schedule_config = {
    "sync_hourly": {
        "task": "logic.sync_logic.run_sync",
        "schedule": crontab(minute=0, hour="*"),
        "options": {
            "expires": 3600,
        },
    },
    # "check_beat_health" तात्पुरतं काढलं
}