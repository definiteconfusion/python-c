import dis

class Objects:
    def __init__(self) -> None:
        self.const_stack=[]
        self.global_stack=[]
        self.optionals=[]
        self.fast={}
        self.rust = ""
        
    def load_global(self, instruction):
        self.global_stack.append(instruction.argval)
    def load_const(self, instruction):
        self.const_stack.append(instruction.argval)
    def call_stack(self):
        cmd_map = {
            "print": self._print(),
            "type": self._type()
            
        }
        if self.global_stack[len(self.global_stack)-1] in cmd_map:
            self.rust += cmd_map[self.global_stack[len(self.global_stack)-1]]
        else:
            pass
    def pop_top(self):
        self.const_stack=[]
        self.global_stack=[]
        pass
    def build_const_key_map(self):
        keys = self.const_table[len(self.const_table)-1]
        values = self.const_table[len(self.const_table)-(len(keys)+1):len(self.const_table)-1]
        del self.const_table[len(self.const_table)-(len(keys)+1):len(self.const_table)]
        self.const_table.append(dict(zip(keys, values)))
        pass
    def list_extend(self):
        itms = list(self.const_table[len(self.const_table)-1])
        self.const_table.pop(len(self.const_table)-1)
        self.const_table.append(itms)
        pass
    def store_fast(self, instruction):
        if instruction.argval not in self.fast:
            self.rust += f'let mut {instruction.argval} = {self.const_stack[len(self.const_stack)-1]};\n'
        else:
            self.rust += f'{instruction.argval} = {self.const_stack[len(self.const_stack)-1]};\n'
        self.fast[instruction.argval] = self.const_stack[len(self.const_stack)-1]
        self.const_stack.pop(len(self.const_stack)-1)
        pass
    def load_fast(self, instruction):
        self.const_stack.append(instruction.argval)
        pass
    def binary_op(self, instruction):
        self.const_stack.append(f'{self.const_stack[len(self.const_stack)-2]} {instruction.argrepr} {self.const_stack[len(self.const_stack)-1]}')
        
    
    def _print(self):
        if not len(self.const_stack) == 0:
            return 'println!("{}", "' + str(self.const_stack[len(self.const_stack) - 1]) + '");\n' if type(self.const_stack[len(self.const_stack) - 1]) == str and self.const_stack[len(self.const_stack) - 1] not in self.fast else 'println!("{}", ' + str(self.const_stack[len(self.const_stack) - 1]) + ');\n'
        else:
            return 'println!("");'
    def _type(self):
        if len(self.const_stack) != 0:
            if "o_type" not in self.optionals:
                self.optionals.append("o_type")
            # This uses the `o_type` function as seen on line 1 of `optional_addons.rs`
            return f'o_type(&{self.const_stack[len(self.const_stack) - 1]});\n'
        else:
            return 'println!("");\n'
    
    
class Compiler:
    def __init__(self, Main) -> None:
        self.Sesh = Objects()
        self.bytec = dis.get_instructions(Main)
        self.rust = ""
        self.cmd_map = {
            "LOAD_CONST": "self.Sesh.load_const(instruction)",
            "LOAD_GLOBAL": "self.Sesh.load_global(instruction)",
            "LOAD_FAST": "self.Sesh.load_fast(instruction)",
            "STORE_FAST": "self.Sesh.store_fast(instruction)",
            "BUILD_CONST_KEY_MAP": "self.Sesh.build_const_key_map()",
            "LIST_EXTEND": "self.Sesh.list_extend()",
            "BINARY_OP": "self.Sesh.binary_op(instruction)",
            "POP_TOP": "self.Sesh.pop_top()",
            "CALL": "self.Sesh.call_stack()"
        }
        
    def compile(self):
        print(self.Sesh.rust)
        for instruction in self.bytec:
            try:
                exec(self.cmd_map[instruction.opname])
            except KeyError:
                pass
            # print("New Instruction")
            # print(instruction.opname, "|" ,instruction.argval, "|" ,type(instruction.argval), "|" ,instruction.argrepr, "\n")
            # print("Stack:", self.Sesh.const_stack)
            # print("Functions:", self.Sesh.global_stack)
            # print("Variables:", self.Sesh.fast, "\n")
        self.rust = self.Sesh.rust