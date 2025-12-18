'''
Lead agent gets access to the list of tools.
It analyzes user request and breaks it down to multiple subtasks.
For each subtask, it picks the right tool for the workers so that they won't have to choose.
It handles the work order to controller. This is the key to dynamic worker spawning!
'''

import json
from src.agents.base import Agent
from src.work.order import WorkOrder
from src.work.state import WorkState
from src.core.context import ContextStore


class LeadAgent(Agent):
    """
    LeadAgent extends the base Agent.
    It can break down user requests into subtasks, assign tools, generate and evaluate work order.
    """

    # user_request comes from context, will update later
    def plan_tasks(self, user_request, tools) -> WorkOrder:
        # 1. Define the System Prompt
        system_instruction = (
            "You are a planning agent. You are given the user's request and a list of tools."
            "Your are to analyze the user's request, break it down into a list of atomic subtasks "
            "and determine which tool is the best tool for each subtask."
            "If no adequate tool is available for a subtask, just say 'no tool available'. "
            "You MUST return your response as a JSON object that strictly "
            "adheres to the provided schema. Do not include any text outside the JSON object."
        )

        # 2. Define the User Prompt
        prompt = f"""
        User Request:
        {user_request}

        Tools Available:
        {tools}

        Return a json following WorkOrder schema.
        """

        # 4. Call the LLM with the schema
        work_order = self.generate_structured(
            messages=[{"role": "user", "content": prompt}],
            tools=tools,
            instructions=system_instruction,
            schema=WorkOrder
        )

        return work_order  # This is an instance of WorkOrder class

    def replan(self, work_order: WorkOrder, work_state: WorkState) -> WorkOrder:
        # Try to reuse the plan_tasks() method
        pass


    def summarize(self, context_store: ContextStore):
        completed_events = [event.content for event in context_store.context.values(
        ) if event.status == "completed"]

        aggregated_input = [{
            "role": "user",
            "content": json.dumps(completed_events)
        }]

        llm_response = self.generate_text(
            messages=aggregated_input,
            instructions="Aggregate and summarize the info. Don't include other texts."
        )

        summary_text = self._extract_text(llm_response)
        print("Lead Agent Report:", summary_text)
        return summary_text


    def _extract_text(self, response):
        texts = []
        for item in response.output:
            if item.type == "message":
                for c in item.content:
                    if hasattr(c, "text"):
                        texts.append(c.text)
        return "\n".join(texts)
