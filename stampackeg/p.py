import pp2
def add(name,greet):
    return f"{greet} {name}!"

c = {"name" : "dvir", "greet": "hello"}

pri()

if __name__ == '__main__':
    print("run from main")
    print(add(**c))
else:
    print("this is not main")