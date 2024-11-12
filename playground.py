@staticmethod
def binary_op(a, b, repr):
    return eval(f"a {repr} b")

print(binary_op(1, 2, "+"))