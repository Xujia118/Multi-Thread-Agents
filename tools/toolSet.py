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
    def search_web(query: str):
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
    def extract_text(url: str):
        pass
