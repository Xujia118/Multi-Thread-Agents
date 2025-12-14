import src.CONSTANTS as CONSTANTS
from src.business_functions.get_weather import get_forecast
from src.business_functions.get_directions import get_directions

"""
When writing tool descriptions for an LLM, remember this: The description is the primary trigger for tool selection.

A professional, high-quality description should ideally include three things:

What the tool does (e.g., calculates area).

What information is required (implicitly or explicitly, e.g., given a length and width).

When to use it (e.g., anytime the user asks for the area)."""


def register(tools):
    @tools.register_tool(
        name=CONSTANTS.CHECK_WEATHER,
        description="Provides the current weather conditions and forecast data for a specified city. Requires the name of the city.",
        parameters={
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    )
    def get_weahter_tool(lat: float, lon: float):
        return get_forecast(lat, lon)

    @tools.register_tool(
        name=CONSTANTS.FIND_DIRECTIONS,
        description="Calculates the route and travel directions between two specific points. Use this when the user asks for directions from one location ('from') to another ('to').",
        parameters={
            "type": "object",
            "properties": {"from": {"type": "string"}, "to": {"type": "string"}},
            "required": ["from", "to"]
        }
    )
    def get_directions_tool(from_: str, to: str):
        return get_directions(from_, to)
    
