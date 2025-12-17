import src.CONSTANTS as CONSTANTS
from src.tools.library.weather import get_forecast
from src.tools.library.hotels import get_hotels

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
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    )
    def get_weahter_tool(location: str):
        return get_forecast(location)

    @tools.register_tool(
        name=CONSTANTS.FIND_DIRECTIONS,
        description="Provides a list of hotels nearby a location. Require the name of the location. Used when searching for hotels.",
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    )
    def get_hotels_tool(location: str):
        return get_hotels(location)
    
