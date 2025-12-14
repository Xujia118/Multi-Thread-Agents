from src.agents.leadAgent import LeadAgent
from src.agents.workerAgent import WorkerAgent
from src.local_tools.toolRegistry import ToolRegistry
from src.local_tools.toolSet import register as register_tools
from src.contextStore import ContextStore
from src.controller import Controller




if __name__ == "__main__":
    # Initialization
    lead_agent = LeadAgent()
    worker_agent = WorkerAgent()

    registry = ToolRegistry()
    register_tools(registry)
    context = ContextStore()

    controller = Controller(
        lead_agent=lead_agent,
        WorkerAgent=WorkerAgent,
        registry=registry,
        context=context,
        max_steps=5
    )
    context = ""

    # Run the pipeline
    user_request = "What's the weather like in Griffith Observatory and how to get there from 28 N 4 ST San Jose?"
    response = controller.run(user_request)
    
    # print("\nFinal Output:")
    # print(response.output_text)

