from src.agents.lead import LeadAgent
from src.agents.worker import WorkerAgent
from src.tools.local_tools.toolRegistry import ToolRegistry
from src.tools.local_tools.toolSet import register as register_tools
from src.core.context import ContextStore
from src.core.controller import Controller
from openai import OpenAI


def main():
    # 1. Setup Infrastructure
    client = OpenAI()
    registry = ToolRegistry()
    register_tools(registry)
    context_store = ContextStore()

    # 2. Setup Agents
    lead_agent = LeadAgent(client)

    # 3. Setup Orchestration
    controller = Controller(
        client=client,
        lead_agent=lead_agent,
        WorkerAgent=WorkerAgent,
        registry=registry,
        context_store=context_store,
        max_steps=5
    )

    # 4. Execution
    user_request = "What's the weather like in Griffith Observatory? Any hotels around to stay?"
    llm_synthesis = controller.run(user_request)
    print(llm_synthesis)

if __name__ == "__main__":
    main()
    
