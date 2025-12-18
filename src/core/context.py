"""
event_1 = {
  "event_id": "e-101",
  "timestamp": "2025-12-16T10:00:03Z",
  "task_name": "check_weather",
  "agent": "worker_weather",
  "status": "completed",
  "content": {
    "location": "Paris, France",
    "summary": "Mild weather, highs around 18°C, low rain chance",
    "raw": "Mostly sunny this week..."
  },
  "refs": {
    "work_order_id": "wo-001",
    "task_name": 0
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
    task_name: str


class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: f"{uuid.uuid4().hex[:6]}")
    time_stamp: datetime = Field(default_factory=lambda: datetime.now())
    task_name: str
    agent: str
    status: Literal["pending", "running", "completed", "failed"]
    content: dict[str, Any]
    refs: Ref


class ContextStore(BaseModel):
    context: dict[str, Event] = Field(default_factory=dict)


    def add_event(self, event: Event) -> str:
        self.context[event.event_id] = event
        return event.event_id


    def get_event(self, event_id: str) -> Event:
        return self.context[event_id]

