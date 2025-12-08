from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class Agent:
    """
    The Agent holds the identity, model configuration, and tools.
    It is responsible for generating the raw response from the LLM.
    """

    def __init__(self, model, tools=None, instructions=""):
        self.client = OpenAI()
        self.model = model
        self.instructions = instructions


    def generate_response(
            self, 
            input_list, 
            tools=None, 
            override_instructions=None,
            response_schema: dict | None = None
        ):
        """
        Single atomic interaction with the LLM.
        The Agent doesn't know *how* to execute tools, only that they exist.
        """
        active_instructions = override_instructions or self.instructions

        # Prepare the response format for JSON Mode
        response_format = {"type": "text"}  # Default to text
        if response_schema:
            response_format = {"type": "json_object",
                               "schema": response_schema}

        response = self.client.responses.create(
            model=self.model,
            tools=tools,
            instructions=active_instructions,
            input=input_list,
            response_format=response_format
        )
        return response

