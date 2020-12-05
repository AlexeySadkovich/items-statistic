from fastapi import FastAPI

from core import routers


app = FastAPI()
app.include_router(routers.router)
