from fastapi import APIRouter

from services.database import crud
from services.database.schemas import QueryCreate

router = APIRouter()


@router.post("/add")
async def add_query(query: QueryCreate):
    """Save query to database and return its id"""
    saved_query = crud.save_query(query)
    return saved_query.id


@router.get("/stat")
async def get_stat():
    pass
