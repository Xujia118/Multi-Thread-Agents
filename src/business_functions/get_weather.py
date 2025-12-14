import requests


NWS_API_BASE = "https://api.weather.gov"
HEADERS = {
    "User-Agent": "my-weather-app/1.0 (your_email@example.com)",
    "Accept": "application/geo+json"
}


def get_grid_point(lat: float, lon: float) -> dict:
    """Get NWS grid info (office, gridX, gridY) for a lat/lon."""
    url = f"{NWS_API_BASE}/points/{lat},{lon}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["properties"]


def get_forecast(lat: float, lon: float) -> list:
    """Get weather forecast periods for a location."""
    grid = get_grid_point(lat, lon)

    forecast_url = grid["forecast"]
    response = requests.get(forecast_url, headers=HEADERS)
    response.raise_for_status()

    return response.json()["properties"]["periods"]

