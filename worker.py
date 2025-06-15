import os
from celery import Celery

# Create Celery app instance
celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
)

# Discover tasks from this module path
celery_app.autodiscover_tasks(["app.api.tasks"])
