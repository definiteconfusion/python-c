# import dis

# def main():
#     x = 1
#     y = x + 14
#     z = y - x
#     a = 30 - 13
#     print(type(z))
#     return "Done"

# for instruction in dis.get_instructions(main):
#         print(instruction.opname, instruction.argval, type(instruction.argval), instruction.argrepr, "\n")
#         # print(instruction, "\n")

from utils import Compiler

def main():
    x = 1
    y = x+5
    z = y-1
    print(z)

compiler = Compiler(main)
compiler.compile()
print(compiler.rust)