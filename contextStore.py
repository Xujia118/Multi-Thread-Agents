from pydantic import BaseModel, Field
from typing import Any
import uuid


class ContextStore(BaseModel):
    session_id: str = Field(default_factory=lambda x: str(uuid.uuid4()))
    context: dict[str, Any] = Field(default_factory=dict)

    def add_to_context(self, event):
        pass


    def get_context(self):
        return self.context
