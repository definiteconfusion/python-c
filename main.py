from utils import Compiler; import dis

def main():
    test = "hello"
    if test=="hello":
        print("Hello")
        print("World")
    print(test)
    return 1
    
# for instruction in dis.get_instructions(main):
#     if instruction.opname != "POP_JUMP_IF_FALSE":
#         print(
#             instruction.opname, instruction.argval, type(instruction.argval),
#             "*", instruction.argrepr.split(" ")[-1], "*", 
#             instruction.positions.lineno, "|", instruction.offset, "\n"
#         )
#     else:
#         print(
#             instruction.opname, instruction.argval, type(instruction.argval),
#             "*", int(instruction.argrepr.split(" ")[-1]), "*", 
#             instruction.positions.lineno, "|", instruction.offset, "\n"
#         )

Compiler(main).compile(
    compiled=True,
    compile_type="development",
    runCompiled=True
)
