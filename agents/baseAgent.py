from openai import OpenAI
from typing import Type
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Agent:
    """
    Based Agent only serves as a parent class for other agents.
    Only model is needed at initialization.
    """
    DEFAULT_MODEL = "gpt-5-mini"

    def __init__(self, model: str | None = None):
        self.client = OpenAI()
        self.model = model or self.DEFAULT_MODEL

    # ============================================================
    # 1) RAW LLM OUTPUT  → for chat, general prompts, creative output
    # ============================================================

    def generate_text(
        self,
        messages: list[dict],
        tools=None,
        instructions=None,
    ):
        return self.client.responses.create(
            model=self.model,
            input=messages,
            tools=tools,
            instructions=instructions
        ).output_text   # ⬅ returns string directly

    # ============================================================
    # 2) STRUCTURED OUTPUT  → validated JSON, WorkOrders, Plans, etc.
    # ============================================================

    def generate_json(
        self,
        messages: list[dict],
        schema: Type[BaseModel],     # ⬅ Pass Pydantic class, not dict
        tools=None,
        instructions=None,
    ):
        response = self.client.responses.parse(
            model=self.model,
            input=messages,
            tools=tools,
            instructions=instructions,
            text_format=schema
        )
        return response.output_parsed   # ⬅ Returns actual Python object
