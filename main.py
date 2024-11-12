from utils import Compiler
import dis

def main():
    name = "Hello, World!"
    print(len(name))
    print(name)

compiler = Compiler(main)
compiler.compile(
    compiled=True,
    runCompiled=True
)

# for instruction in dis.get_instructions(main):
#     print(instruction.opname, instruction.argval, type(instruction.argval), instruction.argrepr)