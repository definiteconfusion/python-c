def call_stack():
        stack = "print", "Hello, World!"
        Commands_obj = Commands(stack[1], type(stack[1]))
        return Commands_obj.cmd_map[stack[0]]
    
class Commands:
    def __init__(self, value, type) -> None:
        self.value = value
        self.type = type
        self.identifier = {
            "int": "%d",
            "float": "%f",
            "str": "%s",
            "bool": "%d",
        }[type.__name__]
        self.cmd_map = {
            "print": self._print(),
        }
        pass
        
    def _print(self):
        return f'printf(\"{self.identifier}\", "{self.value}");'
    
print(call_stack())