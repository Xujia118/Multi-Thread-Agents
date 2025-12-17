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


# Detailed Workflow & Schemas

1. Lead agent creates a work_order (IMMUTABLE)
```
work_order = {
  "work_order_id": "wo-001",
  "goal": "Travel advice for Paris",
  "subtasks": [
    {
      "name": "check_weather",
      "args": { "location": "Paris, France" },
      "tool": "weather_tool",
    },
    {
      "name": "find_hotels",
      "args": { "location": "Paris, France" },
      "tool": "hotel_tool",
    }
  ]
}
```

2. Controller derives work_state (AUTHORITATIVE STATE)
```
work_state = {
  "work_order_id": "wo-001",
  "created_at": "2025-12-16T10:00:00Z",
  "subtask_state": {
    0: {
      "name": "check_weather",
      "status": "pending",
      "event_ids": []
    },
    1: {
      "name": "find_hotels",
      "status": "pending",
      "event_ids": []
    }
  },
  "completed": False
}
```


3. Controller spawns workers 
```
Spawn Worker A → check_weather
Spawn Worker B → find_hotels
```

4. Worker A finishes → returns a work result
```
{
  "task_name": "check_weather",
  "ok": True,
  "data": {
      "summary": "...",
      "raw": {...}
  }
}
```

5. Controller wraps it into an vent

```
event_1 = {
  "event_id": "e-101",
  "timestamp": "2025-12-16T10:00:03Z",
  "task_name": "check_weather",
  "result": "success",
  "agent": "worker_weather",
  "content": {
    "location": "Paris, France",
    "summary": "Mild weather, highs around 18°C, low rain chance",
    "raw": "Mostly sunny this week..."
  },
  "refs": {
    "work_order_id": "wo-001",
    "subtask_index": 0
  }
}
```

Controller pushes the event to context store and updates work_state (NOT the worker)
```
context_store["events"] = [event_1]
work_state["subtask_state"][0]["status"] = "completed"
work_state["subtask_state"][0]["event_ids"].append("e-101")
```

6. If worker B fails
```
{
  "task_name": "find_hotels",
  "ok": False,
  "error": {
      "message": "Hotel API timeout",
      "type": "timeout"
  }
}

```

Controller records the event in context store and updates work state
```
context_store["events"] = [event_2]
work_state["subtask_state"][1]["status"] = "failed"
work_state["subtask_state"][1]["event_ids"].append("e-202")
```

7. Controller sends work state to lead agent for review
At this stage, multithreading is over and the "with" context exits. The controller sends work state to the lead agent, who inspects subtask status. 
It will loop through all subtasks and append failed task to a new work order. 
If the new work order is empty, then we can break loop. Otherwise, we relase the new work order, this time with only failed subtasks. 
Either all status are completed or the max_steps is reached, we send the work state for final summary. 
