from agents.leadAgent import LeadAgent
from agents.workerAgent import WorkerAgent
from tools.toolRegistry import ToolRegistry
from tools.toolSet import register as register_tools
from contextStore import ContextStore
from controller import Controller

if __name__ == "__main__":
    # Initialization
    lead_agent = LeadAgent()
    worker_agent = WorkerAgent()

    registry = ToolRegistry()
    register_tools(registry)

    controller = Controller()
    context = ContextStore()

    # Run the pipeline
    user_request = "What's the weather like in San Diego and how to get there from 28 N 4 ST San Jose?"
    response = controller.run(
                user_request, 
                lead_agent, 
                worker_agent, 
                registry, 
                context
            )
    
    print("\nFinal Output:")
    print(response.output_text)

