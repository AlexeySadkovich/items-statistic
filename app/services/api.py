import requests
from fastapi import HTTPException, status

from core.config import API_KEY

ITEMS_ENDPOINT = "https://m.avito.ru/api/9/items"
LOCATION_ENDPOINT = "https://m.avito.ru/api/1/slocations"


def get_items_count(phrase: str, region: str) -> int:
    """
    Return count of items specified by
     search phrase and region
    :param phrase: search phrase (string)
    :param region: location of searching (string)
    :return: count of items (integer)
    """

    params = {
        "key": API_KEY,
        "locationId": _get_region_id(region),
        "query": phrase,
        "page": 1
    }

    req = requests.get(ITEMS_ENDPOINT, params=params)
    data = req.json()

    return data["result"]["totalCount"]


def _get_region_id(region: str) -> int:
    region_id = 0

    params = {
        "key": API_KEY,
        "q": region
    }

    req = requests.get(LOCATION_ENDPOINT, params=params)
    data = req.json()

    locations = data["result"]["locations"]

    if len(locations) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region for searching not found"
        )

    for location in locations:
        name = location["names"]["1"]
        if name.lower() == region.lower():
            region_id = location["id"]

    return region_id
