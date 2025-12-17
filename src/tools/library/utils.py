import requests
import src.CONSTANTS as CONSTANTS



def geocode(location: str) -> dict:
    """Convert a city name to latitude and longitude using OpenStreetMap Nominatim."""
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={location}"
    response = requests.get(url, headers=CONSTANTS.HEADERS)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError(f"City '{location}' not found")

    return {
        "latitude": float(data[0]["lat"]),
        "longitude": float(data[0]["lon"])
    }

