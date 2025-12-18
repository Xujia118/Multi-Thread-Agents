from pydantic import BaseModel


class WorkResult(BaseModel):
    task_name: str
    tool: str
    ok: bool
    data: dict
    error: dict

    