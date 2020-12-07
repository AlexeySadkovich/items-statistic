from datetime import datetime
from typing import List

from bson import ObjectId

from services.api import get_items_count
from services.database.database import db
from services.database.schemas import QueryCreate, Query


def save_query(query: QueryCreate) -> Query:
    """
    Save query to database
    :param query: consist phrase and region (QueryCreate)
    :return: saved query with id (Query)
    """

    queries = db["queries"]

    query_to_save = {
        "phrase": query.phrase,
        "region": query.region,
        "timestamps": []
    }

    query_to_save["timestamps"].append({
        "time": datetime.now(),
        "count": get_items_count(query.phrase, query.region)
    })

    inserted_id = queries.insert_one(query_to_save).inserted_id

    query_to_save["id"] = inserted_id

    return Query(**query_to_save)


def get_statistic_for_query(query_id: str, time_from: datetime, time_to: datetime) -> List:
    """
    Return counts timestamps for required query
    in the time range specified by parameters
    :param query_id: id of query (str)
    :param time_from: begin of time range (datetime)
    :param time_to: end of time range (datetime)
    :return: list of timestamps which contain time and count
    """
    queries = db["queries"]

    result = []

    saved_query = queries.find_one({"_id": ObjectId(query_id)})
    query_data = Query(**saved_query)

    for ts in query_data.timestamps:
        if not time_from and not time_to:
            break

        if not time_from:
            time_from = datetime(1970, 1, 1)

        if not time_to:
            time_to = datetime.now()

        if time_from <= ts["time"] <= time_to:
            result.append(ts)

    return result


def update_queries_stat():
    """Update statistic for all saved queries"""
    queries = db["queries"]

    for q in queries.find():
        query_data = Query(**q)
        new_statistic = {
            "time": datetime.now(),
            "count": get_items_count(query_data.phrase, query_data.region)
        }

        queries.update_one({"_id": ObjectId(query_data.id)}, {"$push": {"timestamps": new_statistic}})
