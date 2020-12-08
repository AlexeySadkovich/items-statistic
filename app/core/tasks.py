import asyncio

from core.celery import celery
from services.database.crud import update_queries_stat


@celery.task
def update_statistic():
    """Task which call statistic updating"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_queries_stat())
