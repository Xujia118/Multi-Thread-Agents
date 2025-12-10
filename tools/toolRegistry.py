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
        """Return tool object suitable for OpenAI API."""
        # Normalize tool name. openai API returns function.toolname format
        if name.startswith("functions."):
            name = name.replace("functions.", "")
        
        t = self.registry.get(name)
        if not t:
            return None 
        return {
            "type": "function",
            "name": t["name"],
            "description": t["description"],
            "parameters": t["parameters"],
        }
