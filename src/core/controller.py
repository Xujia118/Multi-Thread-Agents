import json
from typing import Any, Type
from src.agents.worker import WorkerAgent
from src.agents.lead import LeadAgent
from src.tools.local_tools.toolRegistry import ToolRegistry
from src.work.order import WorkOrder
from src.work.state import WorkState, SubtaskState
from src.work.result import WorkResult
from src.core.context import Ref, Event, ContextStore
from concurrent.futures import ThreadPoolExecutor, as_completed


class Controller:
    def __init__(self, lead_agent: LeadAgent, WorkerAgent: Type[WorkerAgent], registry: ToolRegistry, context: ContextStore, max_steps=3):
        self.lead_agent = lead_agent
        self.WorkerAgent = WorkerAgent  # class not instance 
        self.registry = registry
        self.context = context
        self.max_steps = max_steps
        self.max_workers = 5  # TODO decide a better default


    def run(self, user_request):
        # PHASE: Planning

        # Step 1: Lead agent receives user request and tools, and returns work order
        print(f"Lead agent processing user query and planning...\n")
        all_tools = self.registry.get_all_tools()
        work_order = self.lead_agent.plan_tasks(user_request, all_tools)

        # Step 2: Controller makes work state from work order
        work_state = WorkState.from_work_order(work_order)

        # PHASE: Execution
        
        steps = 0

        while True:
            # Step 3. Spawn workers to handle subtasks concurrently and return work results
            work_results = self.spawn_workers(work_state, work_order)

            # Step 4: Construct events and update context store
            self.update_work_state_and_context_store(work_state, work_results)

            # Step 5: Lead agent evaluates work state. Is work_state.completed == true?
            decision = self.lead_agent.evaluate_tasks() # TODO: parameters, stuff

            if decision is True: # FINAL, to update semantic
                # Assemble the final summary
                return decision
            
            # Otherwise, make a new work order based on work state and context
            
            steps += 1
            if steps >= self.max_steps:
                return 


    def spawn_workers(self, work_state : WorkState, work_order: WorkOrder) -> list[WorkResult]:
        tasks_to_run = [t for t in work_state.subtasks.values() if t.status != "completed"]
        num_workers_needed = len(tasks_to_run)

        if num_workers_needed == 0:
            print("No new tasks to run.\n")
            return []

        print(f"Spawning {num_workers_needed} worker agents concurrently...\n")

        results: list[WorkResult] = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures_to_subtask = {
                executor.submit(self._execute_subtask, subtask, work_order): subtask 
                for subtask in tasks_to_run
            }

            for future in as_completed(futures_to_subtask):
                original_subtask = futures_to_subtask[future]
                try:
                    work_result = future.result()
                    results.append(work_result)
                    print(f"--- Task Result: '{work_result.task_name}' completed. ok={work_result.ok} ---")
                except Exception as e:
                    print(f"Worker for '{original_subtask.name}' raised an exception: {e}")
                    results.append(
                        WorkResult(
                            task_name=original_subtask.name,
                            tool=original_subtask.tool,
                            ok=False,
                            data={},
                            error={"message": f"Thread exception: {e}"}
                        )
                    )

        return results


    def _execute_subtask(self, subtask: SubtaskState, work_order: WorkOrder) -> WorkResult:
        """
        A helper function to be run concurrently by the ThreadPoolExecutor.
        It runs a single subtask and updates its status/result.
        """
        if subtask.status == "completed":
            return WorkResult(
                task_name=subtask.name,
                tool=subtask.tool,
                ok=True,
                data={},
                error={}
            )
        
        # Retrieve data from work order to keep work state slim
        subtask_def = next(sd for sd in work_order.subtasks if sd.name == subtask.name)
        subtask_args = subtask_def.args
        subtask_tool = subtask_def.tool

        # Create a worker instance
        worker = self.WorkerAgent()

        # Build the worker input message
        worker_input = {
            "task name": subtask.name,
            "task args": subtask_args
        }

        worker_messages = [
            {
                "role": "user",
                "content": json.dumps(worker_input)
            }
        ]

        tool_obj = self.registry.get_tool(subtask_tool)
        if tool_obj is None:
            return WorkResult(
                task_name=subtask.name,
                tool=subtask.tool,
                ok=False,
                data={},
                error={"message": f"Tool {subtask_tool} not found"}
            )

        # Let worker start working!
        try:
            worker_response = worker.run(
                worker_input=worker_messages,
                tool=tool_obj,
                instructions="Use the tool to solve the task.",
                registry=self.registry
            )
            return WorkResult(
                task_name=subtask.name,
                tool=subtask.tool,
                ok=True,
                data={"result": worker_response},
                error={}
            )
        except Exception as e:
            return WorkResult(
                task_name=subtask.name,
                tool=subtask.tool,
                ok=False,
                data={},
                error={"message": str(e)}
            )


    def update_work_state_and_context_store(self, work_state: WorkState, work_results: list[WorkResult]):
        # Step 1 : Create a new Event object and update context store
        for i, result in enumerate(work_results):
            event = Event(
                task_name=result.task_name,
                agent=result.tool,
                status="completed" if result.ok else "failed",
                content=result.data if result.data else result.error,
                refs=Ref(work_order_id=work_state.work_order_id, task_name=result.task_name)
            )
        
        
        # Step 2: Update work state


        pass




        
    def handle_event(self, event):
        wo_id = event.refs["work_order_id"]
        idx = event.refs["subtask_index"]

        runtime = work_runtime_map[wo_id]
        runtime["subtask_state"][idx]["event_ids"].append(event["event_id"])

        if event["type"] == "tool_result":
            runtime["subtask_state"][idx]["status"] = "completed"
