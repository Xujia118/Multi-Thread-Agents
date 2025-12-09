# Goal
Create an agentic system with router and worker llms, capable of answering a precise question
on weather or direction, or answering both and querying in parallel.

The design is the key:
- The number of workers must be dynamic
- The tools must be available to all workers
- Each worker only does its piece of job
- There must be an evaluation step before the final output


# Components & Workflow

1. Controller → LeadAgent(user_request)
2. LeadAgent → work_order
3. Controller spawns workers for subtasks (parallel or batch)
4. Workers execute + return results → Controller
5. Controller stores results → ContextStore, updates work_order.json
6. Controller → LeadAgent(results) for evaluation/summary
7. If LeadAgent says incomplete → generate new work_order for missing parts
8. Else → LeadAgent composes final answer for user

Workers never touch context directly.
Controller orchestrates state.
LeadAgent reasons, not verifies truth.


Lead Agent decides what needs to be done
Controller decides how it is executed