a = []

print(" OR ".join(a) == "")

def test():
    return [ [], [], []]

def test2():
    return [[len(x), x] for x in test()]

print(test2())