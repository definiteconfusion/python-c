import json

tst = [
    "Hello",
    "World"
]

print(json.dumps(tst))
print(type(json.dumps(tst)))
print(type(eval(json.dumps(tst))))