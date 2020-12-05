from bson import ObjectId

from services.database.database import db
from services.database.schemas import QueryCreate, Query


def save_query(query: QueryCreate) -> Query:
    """
    Save query to database
    :param query: consist phrase and region (QueryCreate)
    :return: saved query with id (Query)
    """
    inserted_id = db.insert_one(query).inserted_id

    saved_query = Query()
    saved_query.id = inserted_id
    saved_query.phrase = query.phrase
    saved_query.region = query.region

    return saved_query
