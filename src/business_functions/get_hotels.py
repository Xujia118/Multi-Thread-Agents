import requests
from . utils import geocode


def get_hotels(location: str, limit: int = 10):
    """Get hotels info for lat/lon"""
    coords = geocode(location)
    lat, lon = coords["latitude"], coords["longitude"]

    # lat = 37.3382
    # lon = -121.8863
    radius_meters = 3000  # 3 km

    overpass_query = f"""
    [out:json];
    (
      node["tourism"="hotel"](around:{radius_meters},{lat},{lon});
      way["tourism"="hotel"](around:{radius_meters},{lat},{lon});
    );
    out center tags;
    """

    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=overpass_query,
        timeout=30
    )

    data = response.json()

    hotels = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = tags.get("name")
        if name:
            hotels.append({
                "name": name,
                "address": {
                    "street": tags.get("addr:street"),
                    "city": tags.get("addr:city"),
                    "postcode": tags.get("addr:postcode")
                }
            })

        if len(hotels) >= limit:
            break

    return hotels

