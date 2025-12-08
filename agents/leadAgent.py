'''
Lead agent gets access to the list of tools.
It analyzes user request and breaks it down to multiple subtasks.
For each subtask, it picks the right tool for the workers so that they won't have to choose.
It handles the work order to controller. This is the key to dynamic worker spawning!
'''

from baseAgent import Agent
from workOrder import WorkOrder, Subtask
import json


class LeadAgent(Agent):
    """
    LeadAgent extends the base Agent.
    It can break down user requests into subtasks, assign tools, generate and evaluate work order.
    """

    def __init__(self, model, tools=None, instructions=""):
        super().__init__(model, tools, instructions)
        self.model = "gpt-5-mini"
        self.default_worker_model = "gpt-5-nano"


    # user_request comes from context, will update later
    def plan_tasks(self, user_request) -> WorkOrder:
        # 1. Get the JSON schema from the Pydantic model
        # This describes the structure the LLM must follow.
        work_order_schema = WorkOrder.model_json_schema()

        # 2. Define the System Prompt
        # This tells the LLM what its job is.
        system_instruction = (
            "You are a planning agent. You are given the user's request and a list of tools."
            "Your are to analyze user's request, break it down into a list of atomic subtasks "
            "and determine which tool is the best tool to use for each subtask."
            "If no adequate tool is available for a subtask, just say 'no tool available'. "
            "You MUST return your response as a JSON object that strictly "
            "adheres to the provided schema. Do not include any text outside the JSON object."
        )

        # 3. Define the User Prompt
        prompt = f"User Request: '{user_request}'\n\nBreak this request down into a WorkOrder."

        # 4. Call the LLM with the schema
        raw_response = self.generate_response(
            input_list=[{"role": "user", "content": prompt}],
            override_instructions=system_instruction,
            response_schema=work_order_schema
        )

        # 5. Parse the JSON response and validate it with Pydantic
        try:
            # Assuming the response text is a valid JSON string
            response_json = json.loads(raw_response.choices[0].message.content)
            # Validate the data against the Pydantic schema
            work_order = WorkOrder(**response_json)
            return work_order
        except (json.JSONDecodeError, Exception) as e:
            print(f"Failed to parse or validate WorkOrder: {e}")
            # Handle the failure (e.g., retry, return an empty WorkOrder)
            return WorkOrder(goal=user_request, subtasks=[])


    def create_worker(self):
        pass


    def evaluate_tasks(self):
        prompt = """
        
        """
        pass

    

