from datetime import datetime

import bson
from bson import ObjectId
from fastapi import HTTPException, status

from core.config import TOP_ITEMS_AMOUNT
from services.api import get_items_data
from services.database.database import db
from services.database.schemas import QueryCreate, Query

queries = db["queries"]


async def save_query(query: QueryCreate) -> Query:
    """
    Save query to database
    :param query: consist phrase and region (QueryCreate)
    :return: saved query with id (Query)
    """

    query_to_save = {
        "phrase": query.phrase.lower(),
        "region": query.region.lower(),
        "timestamps": []
    }

    # Check if such phrase and region already saved
    saved_query = await queries.find_one({
        "phrase": query_to_save["phrase"],
        "region": query_to_save["region"]
    })
    if saved_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Such phrase and region already saved"
        )

    items_data = get_items_data(query_to_save["phrase"], query_to_save["region"], TOP_ITEMS_AMOUNT)

    query_to_save["timestamps"].append({
        "time": datetime.now(),
        "count": items_data["count"],
        "top_items": items_data["top"]
    })

    inserted = await queries.insert_one(query_to_save)

    query_to_save["id"] = inserted.inserted_id

    return Query(**query_to_save)


async def get_statistic_for_query(query_id: str, field: str, time_from: datetime, time_to: datetime) -> list:
    """
    Return counts timestamps for required query
    in the time range specified by parameters
    :param query_id: id of query (str)
    :param field: field which should be taken from statistic
    :param time_from: begin of time range (datetime)
    :param time_to: end of time range (datetime)
    :return: list of timestamps which contain time and count
    """

    fields = {"timestamps.time": 1, f"timestamps.{field}": 1}

    try:
        saved_query = await queries.find_one({"_id": ObjectId(query_id)}, fields)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid query ID"
        )

    if not saved_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Query with id {query_id} not found"
        )

    if not time_from and not time_to:
        return saved_query["timestamps"]

    result = []

    for ts in saved_query["timestamps"]:
        if not time_from:
            time_from = datetime(1970, 1, 1)

        if not time_to:
            time_to = datetime.now()

        if time_from <= ts["time"] <= time_to:
            result.append(ts)

    return result


async def update_queries_stat():
    """Update statistic for all saved queries"""
    async for q in queries.find():
        query_data = Query(**q)
        items_data = get_items_data(query_data.phrase, query_data.region, 5)

        new_statistic = {
            "time": datetime.now(),
            "count": items_data["count"],
            "top_items": items_data["top"]
        }

        await queries.update_one({"_id": ObjectId(query_data.id)}, {"$push": {"timestamps": new_statistic}})
