from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectId')
        return ObjectId(v)


class QueryBase(BaseModel):
    phrase: str
    region: str


class QueryCreate(QueryBase):
    pass


class Query(QueryBase):
    id: Optional[PyObjectId] = Field(alias='_id')
    timestamps: List

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
