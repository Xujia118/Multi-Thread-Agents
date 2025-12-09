from openai import OpenAI
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


    def generate_response(
            self, 
            input_list, 
            instructions,
            tools=None, 
            response_schema: dict | None = None
        ):
        """
        Single atomic interaction with the LLM.
        The Agent doesn't know *how* to execute tools, only that they exist.
        """

        # Prepare the response format for JSON Mode
        response_format = {"type": "text"}  # Default to text
        if response_schema:
            response_format = {"type": "json_object",
                               "schema": response_schema}

        response = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            tools=tools,
            input=input_list,
            response_format=response_format
        )
        return response

