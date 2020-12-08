import requests
from fastapi import HTTPException, status

from core.config import API_KEY

ITEMS_ENDPOINT = "https://m.avito.ru/api/9/items"
LOCATION_ENDPOINT = "https://m.avito.ru/api/1/slocations"


def get_items_data(phrase: str, region: str, top_offset: int) -> dict:
    """
    Return count of items specified by
     search phrase and region
    :param phrase: search phrase (string)
    :param region: location of searching (string)
    :param top_offset: amount of top items
    :return: count of items (integer)
    """
    data = _get_items(phrase, region)
    items = data["result"]["items"][:top_offset]

    # Take title and url of top items
    top_items = []
    for item in items:
        value = item["value"]
        # Check for unusual structure of json data
        if "list" in value:
            formatted_item = {
                "title": value["list"][0]["value"]["title"],
                "url": "avito.ru" + value["list"][0]["value"]["uri_mweb"]
            }
        else:
            formatted_item = {
                "title": value["title"],
                "url": "avito.ru" + value["uri_mweb"]
            }

        top_items.append(formatted_item)

    result = {
        "count": data["result"]["totalCount"],
        "top": top_items
    }

    return result


def _get_items(phrase: str, region: str) -> dict:
    params = {
        "key": API_KEY,
        "locationId": _get_region_id(region),
        "query": phrase,
        "page": 1
    }

    req = requests.get(ITEMS_ENDPOINT, params=params)
    data = req.json()

    return data


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
