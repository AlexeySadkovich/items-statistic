from fastapi import APIRouter

router = APIRouter()


@router.post("/add")
async def add_query():
    pass


@router.get("/stat")
async def get_stat():
    pass
