'''
Work state tracks live progress, results and errors.

work_state = {
  "work_order_id": "wo-001",
  "created_at": "2025-12-16T10:00:00Z",
  "subtasks": {
    "check_weather": {
      "name": "check_weather",
      "tool": "weather_tool",
      "status": "pending",
      "event_ids": []
    },
    "find_hotels": {
      "name": "find_hotels",
      "tool": "hotel_tool",
      "status": "pending",
      "event_ids": []
    }
  },
}


Here is the flow:

WorkOrder (immutable spec)
   ↓
WorkState (mutable truth)
   ↓
ContextStore (append-only evidence)

'''


from pydantic import BaseModel, ConfigDict
from typing import Literal
from datetime import datetime
from src.work.result import WorkResult


class SubtaskState(BaseModel):
    """
    Lightweight execution index for a single subtask.

    This class does NOT store execution results or errors.
    All execution facts (outputs, errors, timestamps) are recorded
    as Events and referenced here by event_id.

    Purpose:
    - prevent duplicate execution
    - track ownership ("running")
    - enable safe retries and recovery
    """

    name: str
    tool: str
    status: Literal["pending", "running", "completed", "failed"]
    event_ids: list[str]

    model_config = ConfigDict(extra='forbid')


class WorkState(BaseModel):
    work_order_id: str
    created_at: datetime
    subtasks: dict[str, SubtaskState]

    model_config = ConfigDict(extra='forbid')

    @classmethod
    def from_work_order(cls, work_order):
        return cls(
            work_order_id=work_order.id,
            created_at=datetime.now(),
            subtasks={sub.name : SubtaskState(name=sub.name, tool=sub.tool, status="pending", event_ids=[])
                      for sub in work_order.subtasks}
        )

  
    def update(self, event_id: str, work_results: list[WorkResult]):
      """
      Update this WorkState in place based on a list of WorkResult objects.
      """
      for result in work_results:
          subtask = self.subtasks.get(result.task_name)

          if subtask:
            subtask.status = "completed" if result.ok else "failed"
            subtask.event_ids.append(event_id)


    def get_runnable_subtasks(self) -> list[SubtaskState]:
        runnable_tasks = []

        for t in self.subtasks.values():
           if t.status == "pending":
              runnable_tasks.append(t)

        return runnable_tasks

