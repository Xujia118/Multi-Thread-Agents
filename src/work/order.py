'''
Work order is immutable. It gives a list of subtasks. It doesn't record states.

work_order = {
  "id": 123abc,
  "goal": "Travel advice for NY",
  "subtasks": [
    {
      "name": "check_weather",
      "tool": "weather_tool",
      "args": { "location": "New York" },
    },
    {
      "name": "find_hotels",
      "tool": "hotel_tool",
      "args": { "location": "New York" },
    }
  ]
}
'''


from pydantic import BaseModel, Field, ConfigDict


class SubtaskDefinition(BaseModel):
    name: str
    tool: str
    args: str = Field(description="The arguments for the tool as a JSON string, e.g. '{\"location\": \"NY\"}'")

    # Set additionalProperties to False
    model_config = ConfigDict(extra='forbid')


class WorkOrder(BaseModel):
    id: str
    goal: str
    subtasks: list[SubtaskDefinition]

    model_config = ConfigDict(extra='forbid')
