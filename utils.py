class Objects:
    def __init__(self) -> None:
        self.stack = []
        
    def load_global(self, func_name):
        self.stack.append(func_name)
    def load_const(self, const_value):
        self.stack.append(const_value)
    def call_stack(self):
        return self.stack
    def pop_top(self):
        self.stack=[]
        pass
    
class Caller:
    def __init__(self) -> None:
        self.cmd_map = {
            "LOAD_GLOBAL": Objects().load_global,
            "LOAD_CONST": Objects().load_const,
            "POP_TOP": Objects().pop_top,
        }

class Commands:
    def __init__(self, value, type) -> None:
        self.value = value
        self.type = type
        self.identifier = {
            "int": "%d",
            "float": "%f",
            "str": "%s",
            "bool": "%d",
        }[type]
        pass
        
    def _print(self):
        return f"printf(\"{self.identifier}\", {self.value});"