from datetime import datetime

from fastapi import APIRouter

from services.database import crud
from services.database.crud import update_queries_stat
from services.database.schemas import QueryCreate

router = APIRouter()


@router.post("/add")
async def add_query(query: QueryCreate):
    """
    View for saving new query to database
    :return: id of saved query
    """
    saved_query = await crud.save_query(query)
    return str(saved_query.id)


@router.get("/stat")
async def get_statistic(query_id: str,
                        time_from: datetime = None,
                        time_to: datetime = None):
    """
    View for pulling statistic of the query specified by id
    :return: list of timestamps
    """
    result = await crud.get_statistic_for_query(query_id, "count", time_from, time_to)
    return result


@router.get("/stat/top")
async def get_top_items(query_id: str,
                        time_from: datetime = None,
                        time_to: datetime = None):
    result = await crud.get_statistic_for_query(query_id, "top_items", time_from, time_to)
    return result
