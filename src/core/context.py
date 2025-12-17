"""
event_1 = {
  "event_id": "e-101",
  "timestamp": "2025-12-16T10:00:03Z",
  "task_name": "check_weather",
  "agent": "worker_weather",
  "result": true,
  "content": {
    "location": "Paris, France",
    "summary": "Mild weather, highs around 18°C, low rain chance",
    "raw": "Mostly sunny this week..."
  },
  "refs": {
    "work_order_id": "wo-001",
    "subtask_index": 0
  }
}

"""


import uuid
from typing import Any
from pydantic import BaseModel, Field
from pydantic import BaseModel
from typing import Any, Literal
from datetime import datetime


class Ref(BaseModel):
    work_order_id: str
    subtask_index: int


class Event(BaseModel):
    event_id: str
    time_stamp: datetime
    task_name: str
    agent: str
    result: Literal["success", "failure"]
    content: dict[str, Any]
    refs: Ref


class ContextStore(BaseModel):
    session_id: str = Field(default_factory=lambda x: str(uuid.uuid4()))

    context: dict[str, Any] = Field(default_factory=dict)

    def add_event(self, event):
        pass

    def get_event(self, event_id: str) -> Event:
        pass
