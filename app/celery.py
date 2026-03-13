"""Celery configuration."""
from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()

app = Celery(
    "tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Configuration
# Celery configuration
app.conf.update(
    timezone="UTC",
    enable_utc=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_routes={
        "app.tasks.collect_news_for_all_companies": {"queue": "news_collection"},
        "app.tasks.cleanup_old_articles": {"queue": "maintenance"},
    },
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# Task imports
app.autodiscover_tasks(
    packages=["app.tasks"],
)

# Beat schedule
app.conf.beat_schedule = {
    "collect-news-every-5-minutes": {
        "task": "app.tasks.collect_news_for_all_companies",
        "schedule": 300.0,  # 5 minutes
        "options": {"queue": "news_collection"},
    },
    "cleanup-old-articles-daily": {
        "task": "app.tasks.cleanup_old_articles",
        "schedule": crontab(hour=3, minute=0),  # 3 AM UTC
        "options": {"queue": "maintenance"},
    },
}
