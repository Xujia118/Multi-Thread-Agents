import json
from typing import Any
from src.agents.workerAgent import WorkerAgent


class Controller:
    def __init__(self, lead_agent, WorkerAgent, registry, context, max_steps=3):
        self.lead_agent = lead_agent
        self.WorkerAgent = WorkerAgent # class not instance
        self.registry = registry
        self.context = context
        self.max_steps = max_steps

    def run(self, user_request):

        # TODO: think about stop logic, it shouldn't be a fixed for loop
        for _ in range(self.max_steps):
            # Step 1. Pass user request and tools to lead agent
            all_tools = self.registry.get_all_tools()

            # Step 2. Lead agent returns a work order
            print(f"Lead agent processing user query and planning...")
            work_order = self.lead_agent.plan_tasks(user_request, all_tools)

            # Step 3. Spawn workers to handle subtasks in parallel
            self.spawn_workers(work_order)

            '''
            We can conceive an if else check. If evaluation is passed, we break; else continue, etc.
            '''

            # Step 4. Each worker sends back its operations done, result and status update
            # Update context store and work order here
            # updated_work_order = self.update_work_order_and_context_store()

            # # Step 5. Send update work order to lead agent for evaluation
            # lead_agent.evaluate(updated_work_order)

    def spawn_workers(self, work_order) -> None:
        num_workers_needed = sum([1 for t in work_order.subtasks if t.status != "completed"])
        print(f"Spawning {num_workers_needed} worker agents...")

        for subtask in work_order.subtasks:
            # Create a worker instance
            worker = self.WorkerAgent()

            # Pass subtask and tool to worker
            worker_input = {
                "task name": subtask.name,
                "task args": subtask.args
            }
            
            tool_obj = self.registry.get_tool(subtask.tool)
            if tool_obj is None:
                raise ValueError(f"Tool {subtask.tool} not found in registry")

            print("tool obj:", tool_obj)

            instructions = f"""You are given a task and a tool. Use the tool to solve the task."""

            # Call run() method
            worker_response = worker.run(json.dumps(worker_input), tool_obj, instructions)
            print("Worker response:", worker_response)

            # Update status in work order
            subtask.result = worker_response
            subtask.status = "completed"



    def update_work_order_and_context_store(self):
        pass

    def _get_worker_input(self, subtask) -> dict[str, Any]:
        pass
