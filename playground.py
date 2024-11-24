stack = [
    "Hello World",
    "Hello World"
]

ins = "=="

def compare_op(stack, instruction):
        stemnt = f"{stack[-1]}{instruction}{stack[-1]}"
        stack.pop(len(stack)-1)
        stack.pop(len(stack)-2)
        stack.append(stemnt)
        return stack
print(compare_op(stack, ins))