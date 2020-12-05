from celery import Celery
from celery.schedules import crontab

from .config import UPDATE_STATISTIC_FREQ, REDIS_HOST, REDIS_PORT

BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
celery = Celery("tasks", include=["core.tasks"], broker=BROKER_URL)

celery.conf.beat_schedule = {
    'update-statistic': {
        'task': 'core.tasks.update_statistic',
        'schedule': crontab(minute=f'*/{UPDATE_STATISTIC_FREQ}')
    }
}