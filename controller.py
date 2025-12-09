from typing import Any
from agents.workerAgent import WorkerAgent


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

    def spawn_workers(self, work_order):
        # We don't want to expose all to workers
        # Only what they need to know: subtask and tool
        running_subtasks = []

        for subtask in running_subtasks:
            # Create a worker object
            worker = self.create_worker()

            # Pass in parameters at runtime
            worker_input = self._get_worker_input(subtask)
            tool = registry.get_tool(subtask.tool)
            instructions = f"""You are given a task and a tool. Use the tool to solve the task."""

            worker.run(worker_input, tool, instructions)

        for subtask in work_order.subtasks:
            if subtask.status != "completed":
                running_subtasks.append(running_subtasks)

        return running_subtasks

    def create_worker(self):
        tool = registry.get_tool(subtask.tool)  # TODO: how to properly pass?

        system_instruction = (

        )

        worker_instruction = f"Handle the task with the tool"  # TODO: rewrite the prompt

        return WorkerAgent()

    def update_work_order_and_context_store(self):
        pass

    def _get_worker_input(self, subtask) -> dict[str, Any]:
        pass
