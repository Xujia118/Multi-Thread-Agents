from functools import wraps


class ToolRegistry:
    def __init__(self):
        self.registry = {}

    def register_tool(self, name, description, parameters):
        """Decorator to register a tool function."""
        def decorator(func):
            self.registry[name] = {
                "func": func,
                "name": name,
                "description": description,
                "parameters": parameters
            }

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def get_all_tools(self):
        return [
            {
                "type": "function",
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"],
            }
            for t in self.registry.values()
        ]

    def get_tool(self, name):
        return self.registry.get(name, {}).get("func")
