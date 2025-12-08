# Goal
Create an agentic system with router and worker llms, capable of answering a precise question
on weather or direction, or answering both and querying in parallel.

The design is the key:
- The number of workers must be dynamic
- The tools must be available to all workers
- Each worker only does its piece of job
- There must be an evaluation step before the final output


# Components & Workflow

┌──────────────┐      Decides tasks
│   Router     │───────────────────────────┐
└───────┬──────┘                           │
        │ spawns N workers                 │
        ↓                                  │
┌──────────────────┐  run tasks in parallel│
│   Controller      │──────────────────────┘
│ (execution engine)│
└───┬────────┬─────┘
    │        │
    ▼        ▼
Worker1    Worker2    ... WorkerN
(tool-aware, stateless executors)
    │        │
    └─── results → aggregator → evaluator → final answer


Critically, tools are available to all workers. Each workder must search the right tool based on the task it's assigned to. The tool-picking should be programmed instead of relying on llm generation. 

The lead agent analyzes the task and decompose it into multiple subtasks such as: 
[
    "User wants to know the weather in New York",
    "User wants to know hwo to get from X to Y"
]
It gets the complete tools available
[
    "weather_tool",
    "map_tool",
    ...
]

Retry & self-correction
If any worker agent fails, the evaluator will mark its task "failed" in the work order.

