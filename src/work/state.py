'''
Work state tracks live progress, results and errors.

work_state = {
  "work_order_id": "wo-001",
  "created_at": "2025-12-16T10:00:00Z",
  "completed": False
  "subtasks": {
    0: {
      "name": "check_weather",
      "status": "pending",
      "event_ids": []
    },
    1: {
      "name": "find_hotels",
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


class SubtaskState(BaseModel):
    name: str
    status: Literal["pending", "completed", "failed"]
    event_ids: list[str]

    model_config = ConfigDict(extra='forbid')


class WorkState(BaseModel):
    work_order_id: str
    created_at: datetime
    completed: bool
    subtasks: dict[int, SubtaskState]

    model_config = ConfigDict(extra='forbid')
