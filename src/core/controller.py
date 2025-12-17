import json
from typing import Any, Type
from src.agents.worker import WorkerAgent
from src.agents.lead import LeadAgent
from src.tools.local_tools.toolRegistry import ToolRegistry
from src.work.order import SubtaskDefinition, WorkOrder
from src.work.state import WorkState, SubtaskState
from concurrent.futures import ThreadPoolExecutor, as_completed


class Controller:
    def __init__(self, lead_agent: LeadAgent, WorkerAgent: Type[WorkerAgent], registry: ToolRegistry, context, max_steps=3):
        self.lead_agent = lead_agent
        self.WorkerAgent = WorkerAgent  # class not instance 
        self.registry = registry
        self.context = context
        self.max_steps = max_steps
        self.max_workers = 5  # TODO decide a better default

    def run(self, user_request):
        # PHASE 1: Planning

        # Step 1: Lead agent receives user request and tools, and returns work order
        print(f"Lead agent processing user query and planning...\n")
        all_tools = self.registry.get_all_tools()
        work_order = self.lead_agent.plan_tasks(user_request, all_tools)

        # Step 2: Controller makes work state from work order
        work_state = WorkState.from_work_order(work_order)

        # PHASE 2: Execution
        
        steps = 0
        while True:
            # Step 3. Spawn workers to handle subtasks concurrently
            self.spawn_workers(work_state)
            # But here, workers should return work results to controller
            # controller will construct events and update context store
            # but here it's multithreading, so how to return work_result?
            
            # Then, controller should update work state and 
            # Also constructs events and updates context store

            # The lead agent evaluates work state. work_state.completed == true?
            decision = self.lead_agent.evaluate_tasks() # TODO: parameters, stuff

            if decision is True: # FINAL, to update semantic
                return decision
            
            steps += 1
            if steps >= self.max_steps:
                return 


    def spawn_workers(self, work_state) -> None:
        tasks_to_run = [t for t in work_state.subtasks if t.status != "completed"]
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


    def _execute_subtask(self, subtask: SubtaskDefinition) -> 'SubtaskDefinition':
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

        
    def handle_event(self, event):
        wo_id = event.refs["work_order_id"]
        idx = event.refs["subtask_index"]

        runtime = work_runtime_map[wo_id]
        runtime["subtask_state"][idx]["event_ids"].append(event["event_id"])

        if event["type"] == "tool_result":
            runtime["subtask_state"][idx]["status"] = "completed"
