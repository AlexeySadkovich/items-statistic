from core.celery import celery
from services.database.crud import update_queries_stat


@celery.task
def update_statistic():
    """Task which call statistic updating"""
    update_queries_stat()
