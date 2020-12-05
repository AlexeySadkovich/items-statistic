import requests

ITEMS_ENDPOINT = "https://m.avito.ru/api/9/items"
LOCATION_ENDPOINT = "https://m.avito.ru/api/1/slocations"
API_KEY = "af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"


def get_items_count(query: str, region: str) -> int:
    """
    Return count of items specified by
     search phrase and region
    :param query: search phrase (string)
    :param region: location of searching (string)
    :return: count of items (integer)
    """

    params = {
        "key": API_KEY,
        "locationId": _get_region_id(region),
        "query": query,
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

    for location in locations:
        if location["name"].lower() == region.lower():
            region_id = location["id"]

    return region_id
