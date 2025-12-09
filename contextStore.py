from pydantic import BaseModel
from typing import Any
from workOrder import WorkOrder


class ContextStore(BaseModel):
    session_id: str
    context: dict[str, Any] = {}
    

    def add_to_context(self, event):
        pass


    def get_context(self):
        return self.context
