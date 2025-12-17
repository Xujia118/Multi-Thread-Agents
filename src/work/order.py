'''
Work order is immutable. It gives a list of subtasks. It doesn't record states.

work_order = {
  "work_order_id": 123abc,
  "goal": "Travel advice for NY",
  "subtasks": [
    {
      "name": "check_weather",
      "tool": "weather_tool",
      "args": { "location": "New York" },
    },
    {
      "name": "find_route",
      "tool": "map_tool",
      "args": { "from": "San Jose", "to": "New York" },
    }
  ]
}
'''


from pydantic import BaseModel, ConfigDict


class SubtaskDefinition(BaseModel):
    name: str
    tool: str
    args: dict 

    # Set additionalProperties to False
    model_config = ConfigDict(extra='forbid')


class WorkOrder(BaseModel):
    work_order_id: str
    goal: str
    subtasks: list[SubtaskDefinition]

    model_config = ConfigDict(extra='forbid')

