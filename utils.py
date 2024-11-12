import dis
import subprocess
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
            self.global_stack.pop(len(self.global_stack)-1)
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
            self.rust += f'let mut {instruction.argval} = {self.const_stack[len(self.const_stack)-1]}\n'
        else:
            self.rust += f'{instruction.argval} = {self.const_stack[len(self.const_stack)-1]}\n'
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
            val = str(self.const_stack[len(self.const_stack) - 1])
            has_operator = any(op in val for op in ['+', '-', '*', '/', '%'])
            needs_quotes = not has_operator and val not in self.fast and not val.startswith('o_type') and type(self.const_stack[len(self.const_stack) - 1]) == str
            return f'println!("{{}}", {("\"" + val + "\"") if needs_quotes else val})\n'
        else:
            return 'println!("")\n'
    def _type(self):
        if len(self.const_stack) != 0:
            if "o_type" not in self.optionals:
                self.optionals.append("o_type")
            # This uses the `o_type` function as seen on line 1 of `optional_addons.rs`
            self.const_stack.append(f'o_type(&{self.const_stack[len(self.const_stack) - 1]})')
            return ""
        else:
            self.const_stack.append('println!("")\n')
            return "NaN"
    
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
    def compile(self, compiled=False, output=False, printed=False, runCompiled=False):
        for instruction in self.bytec:
            try:
                exec(self.cmd_map[instruction.opname])
            except KeyError:
                pass
        self.rust = f"""
#![allow(warnings)]
fn main() {{
{'\n'.join(line.rstrip() + ';' for line in self.Sesh.rust.splitlines())}
}}
        """
        if compiled:
            with open("main.rs", "w") as f:
                f.write(self.rust)
            subprocess.run(["rustc", "main.rs"])
        if runCompiled:
            print(subprocess.run(["./main"], text=True, check=True, capture_output=True).stdout)
        if output:
            return self.rust
        if printed:
            print(self.rust)