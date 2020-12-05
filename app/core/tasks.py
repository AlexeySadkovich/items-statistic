from core.celery import celery


@celery.task
def update_statistic():
    pass
