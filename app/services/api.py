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
    # items = data["result"]["items"]

    # items_list = []
    # item_index = 0
    # while item_index <= top_offset:
    #     item = items[item_index]
    #     if item["type"] == "item":
    #         print("da zaebalo suka")
    #         items_list.append({
    #             "title": item["value"]["title"],
    #             "url": "avito.ru" + item["value"]["uri_mweb"]
    #         })
    #         item_index += 1

    result = {
        "count": data["result"]["totalCount"],
        "top": data["result"]["items"][:top_offset]
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
