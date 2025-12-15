import requests


NWS_API_BASE = "https://api.weather.gov"
HEADERS = {
    "User-Agent": "my-weather-app/1.0 (xujia@hotmail.com)",
    "Accept": "application/geo+json"
}


def get_grid_point(lat: float, lon: float) -> dict:
    """Get NWS grid info (office, gridX, gridY) for a lat/lon."""
    url = f"{NWS_API_BASE}/points/{lat},{lon}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["properties"]


def geocode(location: str) -> dict:
    """Convert a city name to latitude and longitude using OpenStreetMap Nominatim."""
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={location}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    
    if not data:
        raise ValueError(f"City '{location}' not found")
    
    return {
        "latitude": float(data[0]["lat"]),
        "longitude": float(data[0]["lon"])
    }


def get_forecast(location: str) -> list:
    """Get weather forecast periods for a city name or location string."""

    # 1️⃣ Convert city name to lat/lon
    coords = geocode(location)
    lat, lon = coords["latitude"], coords["longitude"]

    # 2️⃣ Get NWS grid info
    grid = get_grid_point(lat, lon)

    # 3️⃣ Get forecast
    forecast_url = grid["forecast"]
    response = requests.get(forecast_url, headers=HEADERS)
    response.raise_for_status()
    periods = response.json()["properties"]["periods"]

    return periods
