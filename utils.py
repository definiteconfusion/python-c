import dis
import subprocess
import json
class Objects:
    """
    A class to handle Python bytecode translation to Rust code.
    This class maintains various stacks and state information needed for the translation process,
    including constant values, global variables, and generated Rust code.
    Attributes:
        const_stack (list): Stack for storing constant values
        global_stack (list): Stack for storing global variable names
        optionals (list): List of optional features/imports needed
        fast (dict): Dictionary for storing local variables
        rust (str): Generated Rust code output
    Methods:
        load_global(instruction): Handles loading of global names
        load_const(instruction): Handles loading of constant values
        call_stack(): Processes function calls from the global stack
        pop_top(): Clears the constant and global stacks
        build_const_key_map(): Builds a dictionary from keys and values on const_table
        list_extend(): Extends a list with items from const stack
        build_list(instruction): Builds a list with specified number of items
        store_fast(instruction): Stores a local variable with type inference
        load_fast(instruction): Loads a local variable onto const stack
        binary_op(instruction): Handles binary operations
        _print(): Handles print function translation
        _type(): Handles type() function translation
        _str(): Handles str() function translation
    """
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
            "print": self._print,
            "type": self._type,
            "str": self._str,
            "len": self._len
        }
        if self.global_stack[-1] in cmd_map:
            result = cmd_map[self.global_stack[-1]]()
            if result:
                self.rust += result
            self.global_stack.pop()
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
        itms = list(self.const_stack[len(self.const_stack)-1])
        self.const_stack.pop(len(self.const_stack)-1)
        self.const_stack.append((json.dumps(itms), 'Operator'))
        pass
    def build_list(self, instruction):
        if instruction.argval == 0:
            pass
        elif instruction.argval == 1:
            self.const_stack.append((json.dumps([self.const_stack[len(self.const_stack)-1]]), 'Operator'))
        elif instruction.argval == 2:
            self.const_stack.append((json.dumps([self.const_stack[len(self.const_stack)-2], self.const_stack[len(self.const_stack)-1]]), 'Operator'))
    def store_fast(self, instruction):
        if instruction.argval not in self.fast:
            if type(self.const_stack[len(self.const_stack)-1])  == int:
                bits = len(bin(self.const_stack[len(self.const_stack)-1])[2:])
                if bits <= 31:
                    int_type = 32
                elif bits <= 63:
                    int_type = 64
                else:
                    int_type = 128
                self.rust += f'let mut {instruction.argval}: i{int_type} = {self.const_stack[len(self.const_stack)-1]}\n'
            elif type(self.const_stack[len(self.const_stack)-1]) == float:
                value = abs(self.const_stack[len(self.const_stack)-1])
                if value < 3.4e38:
                    fl_type = 32
                else:
                    fl_type = 64
                self.rust += f'let mut {instruction.argval}: f{fl_type} = {self.const_stack[len(self.const_stack)-1]}\n'
            elif type(self.const_stack[len(self.const_stack)-1]) == str:
                self.rust += f'let mut {instruction.argval} = "{self.const_stack[len(self.const_stack)-1]}"\n'
            elif type(self.const_stack[len(self.const_stack)-1]) == tuple and self.const_stack[len(self.const_stack)-1][1] == 'Operator':
                self.rust += f'let mut {instruction.argval} = {self.const_stack[len(self.const_stack)-1][0]}\n'
            else:
                self.rust += f'let mut {instruction.argval} = {self.const_stack[len(self.const_stack)-1]}\n'
        else:
            self.rust += f'{instruction.argval} = {self.const_stack[len(self.const_stack)-1]}\n'
        self.fast[instruction.argval] = self.const_stack[len(self.const_stack)-1]
        self.const_stack.pop(len(self.const_stack)-1)
        pass
    def load_fast(self, instruction):
        self.const_stack.append((instruction.argval, 'Operator'))
        pass
    def binary_op(self, instruction):
        self.const_stack.append(f'{self.const_stack[len(self.const_stack)-2]} {instruction.argrepr} {self.const_stack[len(self.const_stack)-1]}')
        
    def _print(self):
        if not len(self.const_stack) == 0:
            if type(self.const_stack[len(self.const_stack) - 1]) == tuple and self.const_stack[len(self.const_stack) - 1][1] == 'Operator':
                return f'println!("{{:?}}", {self.const_stack[len(self.const_stack) - 1][0]})\n'
            else:
                return f'println!("{{:?}}", "{self.const_stack[len(self.const_stack) - 1]}")\n'
        else:
            return 'println!("")\n'
    def _type(self):
        if len(self.const_stack) != 0:
            if "o_type" not in self.optionals:
                self.optionals.append("o_type")
            if type(self.const_stack[len(self.const_stack) - 1]) == tuple and self.const_stack[len(self.const_stack) - 1][1] == 'Operator':
                self.const_stack.append((f'o_type(&{self.const_stack[len(self.const_stack) - 1][0]})', 'Operator'))
            else:
                self.const_stack.append((f'o_type(&{self.const_stack[len(self.const_stack) - 1]})', 'Operator'))
            return ""
        else:
            self.const_stack.append('println!("")\n')
            return "NaN"
    def _str(self):
        if len(self.const_stack) != 0:
            if type(self.const_stack[len(self.const_stack) - 1]) == tuple and self.const_stack[len(self.const_stack) - 1][1] == 'Operator':
                self.const_stack.append((f'{self.const_stack[len(self.const_stack) - 1][0]}.to_string()', 'Operator'))
            else:
                self.const_stack.append((f'{self.const_stack[len(self.const_stack) - 1]}.to_string()', 'Operator'))
            return ""
        else:
            self.const_stack.append('println!("")\n')
            return "NaN"
    def _len(self):
        if len(self.const_stack) != 0:
            if type(self.const_stack[len(self.const_stack) - 1]) == tuple and self.const_stack[len(self.const_stack) - 1][1] == 'Operator':
                self.const_stack.append((f'{self.const_stack[len(self.const_stack) - 1][0]}.len()', 'Operator'))
            else:
                self.const_stack.append((f'{self.const_stack[len(self.const_stack) - 1]}.len()', 'Operator'))
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
            "BUILD_LIST": "self.Sesh.build_list(instruction)",
            "BINARY_OP": "self.Sesh.binary_op(instruction)",
            "POP_TOP": "self.Sesh.pop_top()",
            "CALL": "self.Sesh.call_stack()"
        }
        self.optionals = {
            "o_type": "fn o_type<T>(t: &T) -> String {\n    std::any::type_name::<T>().to_string()\n}"
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
{'\n'.join([self.optionals[optional] for optional in self.Sesh.optionals])}
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