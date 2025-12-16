import json
from typing import Any, Type
from src.agents.workerAgent import WorkerAgent
from src.local_tools.toolRegistry import ToolRegistry
from src.workOrder import Subtask, WorkOrder
from concurrent.futures import ThreadPoolExecutor, as_completed


class Controller:
    def __init__(self, lead_agent, WorkerAgent: Type[WorkerAgent], registry: ToolRegistry, context, max_steps=3):
        self.lead_agent = lead_agent
        self.WorkerAgent = WorkerAgent  # class not instance
        self.registry = registry
        self.context = context
        self.max_steps = max_steps
        self.max_workers = 5  # TODO decide a better default

    def run(self, user_request):

        # TODO: think about stop logic, it shouldn't be a fixed for loop
        for _ in range(self.max_steps):
            # Step 1. Pass user request and tools to lead agent
            all_tools = self.registry.get_all_tools()

            # Step 2. Lead agent returns a work order
            print(f"Lead agent processing user query and planning...\n")
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
        tasks_to_run = [t for t in work_order.subtasks if t.status != "completed"]
        num_workers_needed = len(tasks_to_run)

        if num_workers_needed == 0:
            print("No new tasks to run.\n")
            return

        print(f"Spawning {num_workers_needed} worker agents concurrently...\n")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_subtask = {
                executor.submit(self._execute_subtask, subtask): subtask 
                for subtask in tasks_to_run
            }

            for future in as_completed(future_to_subtask):
                original_subtask = future_to_subtask[future]
                try:
                    updated_subtask = future.result()
                    print(f"--- Task Result: '{updated_subtask}' | Status: {updated_subtask.status} ---")
                except Exception as e:
                    print(f"Worker for '{original_subtask}' generated an exception: {e}")
                    original_subtask.status = "faile (thread error)}"
                    original_subtask.result = str(e)


    def _execute_subtask(self, subtask: Subtask) -> 'Subtask':
        """
        A helper function to be run concurrently by the ThreadPoolExecutor.
        It runs a single subtask and updates its status/result.
        """
        if subtask.status == "completed":
            return subtask

        # Create a worker instance
        worker = self.WorkerAgent()

        # Build the worker input message
        worker_input = {
            "task name": subtask.name,
            "task args": subtask.args
        }

        worker_messages = [
            {
                "role": "user",
                "content": json.dumps(worker_input)
            }
        ]

        tool_obj = self.registry.get_tool(subtask.tool)
        if tool_obj is None:
            # Note: This will raise an exception in the worker thread.
            # We should handle it within the thread to update the subtask status.
            print(f"Error: Tool {subtask.tool} not found for subtask {subtask.name}")
            subtask.status = "failed"
            subtask.result = f"Tool not found: {subtask.tool}"
            return subtask

        # Call run() method
        instructions = f"""You are given a task and a tool. Use the tool to solve the task."""
        try:
            worker_response = worker.run(
                worker_input=worker_messages,
                tool=tool_obj,
                instructions=instructions,
                registry=self.registry
            )
            subtask.result = worker_response
            subtask.status = "completed"
            print(f"Worker for '{subtask.name}' completed.")
        except Exception as e:
            subtask.result = str(e)
            subtask.status = "failed"
            print(f"Worker for '{subtask.name}' failed with error: {e}")

        return subtask


    def update_work_order_and_context_store(self):
        pass


    def _get_worker_input(self, subtask) -> dict[str, Any]:
        pass
