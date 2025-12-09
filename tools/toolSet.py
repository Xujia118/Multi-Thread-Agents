import CONSTANTS


def register(tools):
    @tools.register_tool(
        name=CONSTANTS.CHECK_WEATHER,
        description="Search a dedicated weather api",
        parameters={
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    )
    def check_weather(query: str):
        print("weather tool is called!")
        pass

    @tools.register_tool(
        name=CONSTANTS.FIND_DIRECTIONS,
        description="Find directions on a dedicated map api",
        parameters={
            "type": "object",
            "properties": {"from": {"type": "string"}, "to": {"type": "string"}},
            "required": ["from", "to"]
        }
    )
    def get_map(url: str):
        print("map tool is called!")
        pass
