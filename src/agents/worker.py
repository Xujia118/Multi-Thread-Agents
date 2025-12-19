from .base import Agent


class WorkerAgent(Agent):
    """
    WorkerAgent extends from BaseAgent, but has a lower model.
    """
    DEFAULT_WORKER_MODEL = "gpt-5-nano"

    def __init__(self, client, model=None):
        super().__init__(client, model or self.DEFAULT_WORKER_MODEL)


    def run(self, worker_input, tool, instructions, registry):
        """
        Worker runs exactly one subtask with its assigned tools.
        """
        response = self.generate_text(
            worker_input, 
            tools=[tool], 
            instructions=instructions
        )

        return self.handle_tool_call(response, registry)

