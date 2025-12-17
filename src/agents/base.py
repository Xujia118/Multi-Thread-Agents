from openai import OpenAI
from typing import Type, TypeVar
from pydantic import BaseModel
from dotenv import load_dotenv
import json

load_dotenv()

T = TypeVar("T", bound=BaseModel)

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
        )

    # ============================================================
    # 2) STRUCTURED OUTPUT  → validated JSON, WorkOrders, Plans, etc.
    # ============================================================

    def generate_structured(
        self,
        messages: list[dict],
        schema: Type[T],     # ⬅ Pass Pydantic class, not dict
        tools=None,
        instructions=None,
    ) -> T:
        response = self.client.responses.parse(
            model=self.model,
            input=messages,
            tools=tools,
            instructions=instructions,
            text_format=schema
        )

        if response.output_parsed is None:
            raise ValueError("Model failed to generate structured output.")
        
        return response.output_parsed   # ⬅ Returns actual Python object
   
    # ============================================================
    # 3) HANDLE TOOL CALL 
    # ============================================================

    def handle_tool_call(self, response, registry) -> str:
        """
        If the model issued a function_call, execute the tool and return 
        the final summarized text. Otherwise, return output_text.
        """
        tool_call = None
        for item in response.output:
            if item.type == "function_call":
                tool_call = item
                break

        # No tool call → return text directly
        if tool_call is None:
            return response.output_text

        # Execute the tool
        args = json.loads(tool_call.arguments)
        tool_result = registry.execute(
            tool_call.name,
            **args
        )

        # Send tool result back to model for final summary
        followup = self.generate_text(
            messages=[
                {
                    "role": "assistant",
                    "content": json.dumps(tool_result),
                }
            ],
            instructions="""
            Summarize the tool result clearly for the user.
            Always produce a final answer.
            """
        )

        return followup.output_text

