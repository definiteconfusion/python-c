class Objects:
    def __init__(self) -> None:
        self.stack = []
        
    def load_global(self, glob_name):
        self.stack.append(glob_name)
    def load_const(self, const_value):
        self.stack.append(const_value)
    def call_stack(self):
        stack = self.stack
        Commands_obj = Commands(stack[1], type(stack[1]))
        return Commands_obj.cmd_map[stack[0]]
    def pop_top(self):
        self.stack=[]
        pass
    

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
        return f"printf(\"{self.identifier}\", {self.value});"