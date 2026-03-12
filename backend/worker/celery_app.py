from celery import Celery
from backend.app.core.config import settings

celery = Celery(
    "multi-agent-rag",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["backend.app.ingestion.pipeline"],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    worker_prefetch_multiplier=1,
)
