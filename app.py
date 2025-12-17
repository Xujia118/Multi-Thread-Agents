from src.agents.lead import LeadAgent
from src.agents.worker import WorkerAgent
from src.tools.local_tools.toolRegistry import ToolRegistry
from src.tools.local_tools.toolSet import register as register_tools
from src.core.context import ContextStore
from src.core.controller import Controller


if __name__ == "__main__":
    # Initialization
    lead_agent = LeadAgent()

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
    context = "" # Placeholder

    # Run the pipeline
    user_request = "What's the weather like in Griffith Observatory? Any hotels around to stay?"
    response = controller.run(user_request)
    
    # print("\nFinal Output:")
    # print(response.output_text)

