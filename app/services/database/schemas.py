from typing import List

from bson import ObjectId
from pydantic import BaseModel


class Query(BaseModel):
    _id: ObjectId
    phrase: str
    region: str


class QueryStat(Query):
    timestamps: List
