from utils import Compiler

def main():
    x = 1
    y = x + 14
    z = y - x
    print(2*4)
    print(2+4)
    a = type(z)
    print(type(z))
    print("Hello World")
    print(1)
    print(z)

compiler = Compiler(main)
compiler.compile()
print(compiler.rust)