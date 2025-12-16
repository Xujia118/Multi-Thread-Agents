import requests
import src.CONSTANTS as CONSTANTS
from . utils import geocode


def get_grid_point(lat: float, lon: float) -> dict:
    """Get NWS grid info (office, gridX, gridY) for a lat/lon."""
    
    url = f"{CONSTANTS.NWS_API_BASE}/points/{lat},{lon}"
    response = requests.get(url, headers=CONSTANTS.HEADERS)
    response.raise_for_status()
    
    return response.json()["properties"]


def get_forecast(location: str) -> list:
    """Get weather forecast periods for a city name or location string."""

    # Convert city name to lat/lon
    coords = geocode(location)
    lat, lon = coords["latitude"], coords["longitude"]

    # Get NWS grid info
    grid = get_grid_point(lat, lon)

    # Get forecast
    forecast_url = grid["forecast"]
    response = requests.get(forecast_url, headers=CONSTANTS.HEADERS)
    response.raise_for_status()
    periods = response.json()["properties"]["periods"]

    return periods

