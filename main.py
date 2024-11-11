import dis

def main():
    print("Hello World!")
    print("Hola Mundo!")
    return "Done"

for instruction in dis.get_instructions(main):
        print(instruction.opname, instruction.argval, "\n")