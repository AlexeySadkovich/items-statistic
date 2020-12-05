from typing import List

from bson import ObjectId
from pydantic import BaseModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)


class QueryBase(BaseModel):
    phrase: str
    region: str


class QueryCreate(QueryBase):
    pass


class Query(QueryBase):
    id: PyObjectId

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }


class QueryStat(QueryBase):
    timestamps: List
