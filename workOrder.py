'''
work_order = {
  "goal": "Travel advice for NY",
  "subtasks": [
    {
      "name": "check_weather",
      "args": { "location": "New York" },
      "tool": "weather_tool",
      "result": "xxx",
      "status": "pending"
    },
    {
      "name": "find_route",
      "args": { "from": "San Jose", "to": "New York" },
      "tool": "map_tool",
      "result": "xxx",
      "status": "pending"
    }
  ]
}
'''

from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class Subtask(BaseModel):
    name: str
    tool: str
    args: str = Field(description="The arguments for the tool as a JSON string, e.g. '{\"location\": \"NY\"}'")
    result: str | None
    status: str = "pending"  # "pending", "completed", "failed"

    # Set additionalProperties to False
    model_config = ConfigDict(extra='forbid')


class WorkOrder(BaseModel):
    goal: str
    subtasks: list[Subtask]

    model_config = ConfigDict(extra='forbid')

    def update_subtask_result(self, subtask_name: str, result: Any, status: str):
        for subtask in self.subtasks:
            if subtask.name == subtask_name:
                subtask.result = result
                subtask.status = status
                break


    def get_subtask_result(self, subtask_name: str):
        for subtask in self.subtasks:
            if subtask.name == subtask_name:
                return subtask.result
        return None


    def get_failed_subtasks(self) -> list[Subtask]:
        return [st for st in self.subtasks if st.status == "failed"]

