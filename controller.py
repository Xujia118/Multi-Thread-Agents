import json
from agents.workerAgent import WorkerAgent

class Controller:
    def __init__(self) -> None:
        self.MAX_STEPS = 3

    def run(self, user_request, lead_agent, worker_agent, registry, context, max_steps=0):
        steps = 0

        while steps < self.MAX_STEPS:
            # Step 1. Pass user request to lead agent
            work_order_json = lead_agent.plan_tasks(user_request)
            running_subtasks = self.read_work_order(work_order_json)

            # Step 2. Spin up worker agents and they run in parallel
            for subtask in running_subtasks:
                worker = self.create_worker(subtask) # Pass in constructor or in method?
                worker.run() 

            # Step 3. Each worker sends back its operations done, result and status update
            # Update context store and work order here
            updated_work_order = self.update_work_order_and_context_store()

            # Step 4. Send update work order to lead agent for evaluation
            lead_agent.evaluate(updated_work_order)


            pass

    
    def read_work_order(self, work_order_json):
        # Read work order and filter uncompleted subtasks
        work_order = json.loads(work_order_json)

        running_subtasks = []

        for subtask in work_order.subtasks:
            if subtask.status != "completed":
                running_subtasks.append(running_subtasks)
        
        return running_subtasks


    def create_worker(self, subtask):
        tool = registry.get_tool(subtask.tool) # TODO: how to properly pass?

        system_instruction = (

        )

        worker_instruction = f"Handle the task with the tool" # TODO: rewrite the prompt

        return WorkerAgent(tool=tool, instructions=worker_instruction)


    def update_work_order_and_context_store(self):
        pass