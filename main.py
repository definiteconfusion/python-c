from utils import Compiler
import dis

def main():
    strnum = "123"
    num = 123
    print(type(strnum))
    print(type(str(num)))

compiler = Compiler(main)
compiler.compile(
    compiled=True,
    runCompiled=True
)

# for instruction in dis.get_instructions(main):
#     print(instruction.opname, instruction.argval, type(instruction.argval), instruction.argrepr)