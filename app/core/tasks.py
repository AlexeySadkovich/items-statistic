from core.celery import celery
from services.database.crud import update_queries_stat


@celery.task
def update_statistic():
    update_queries_stat()
