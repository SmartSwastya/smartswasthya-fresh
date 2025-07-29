# ╔════════════════════════════════════════════════════╗
# ║             CELERY WORKER WRAPPER (Runner)        ║
# ╚════════════════════════════════════════════════════╝
from celery_app import celery_app

if __name__ == "__main__":
    # 👇 You can tune log level or concurrency from ENV or override here
    celery_app.worker_main(argv=["worker", "--loglevel=info", "--concurrency=4"])

