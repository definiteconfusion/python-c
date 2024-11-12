from utils import Compiler; import dis

def main():
    name = ["Daniel", "John", "Doe"]
    name.append("Kevin")
    print(name)

compiler = Compiler(main)
compiler.compile(
    compiled=True,
    compile_type="development",
    runCompiled=True
)

# for instruction in dis.get_instructions(main):
#     print(instruction.opname, instruction.argval, type(instruction.argval), instruction.argrepr, instruction.positions.lineno)