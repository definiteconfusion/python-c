from utils import Compiler

def main():
    x = 2 * 2
    y = 3
    z = x + y
    print(z)

compiler = Compiler(main)
compiler.compile(
    compiled=True,
    printed=True
)