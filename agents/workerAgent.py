from baseAgent import Agent

class WorkerAgent(Agent):

    """
    WorkerAgent extends from BaseAgent. 
    It receives a subtask and a tool, and runs.
    """

    def __init__(self, model, tools=None, instructions=""):
        super().__init__(model, tools, instructions)

