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
    status: Literal["pending", "running", "completed", "failed"]
    event_ids: list[str]

    model_config = ConfigDict(extra='forbid')


class WorkState(BaseModel):
    work_order_id: str
    created_at: datetime
    completed: bool
    subtasks: dict[int, SubtaskState]

    model_config = ConfigDict(extra='forbid')

    @classmethod
    def from_work_order(cls, work_order):
        return cls(
            work_order_id=work_order.id,
            created_at=datetime.now(),
            completed=False,
            subtasks={i: SubtaskState(name=sub.name, status="pending", event_ids=[])
                      for i, sub in enumerate(work_order.subtasks)}
        )
