from baseAgent import Agent


class WorkerAgent(Agent):
    """
    WorkerAgent extends from BaseAgent, but has a lower model.
    At runtime, it receives a subtask and the necessary tool(s) for that subtask.
    """
    DEFAULT_WORKER_MODEL = "gpt-5-nano"

    def __init__(self, model=None):
        super().__init__(model or self.DEFAULT_WORKER_MODEL)


    def run(self, subtask, tool, instructions):
        """
        Worker runs exactly one subtask with its assigned tool.
        """
        input_list = [{"role": "user", "content": subtask}]
        return self.generate_response(
            input_list, 
            tools=[tool], 
            instructions=instructions
        )

