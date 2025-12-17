from pydantic import BaseModel


class WorkResult(BaseModel):
    task_name: str
    ok: bool
    data: dict
    error: dict

    