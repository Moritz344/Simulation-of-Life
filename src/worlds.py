def world_1():
    # Exponentieller Wachstum mit Bakterien
    # Formel: n(t) = n0 * p%(t)
    t: int = 0
    p: float = 1.15
    n: int = 100
    while t < 5:
        t += 1
        result = n * p ** t
        result = round(result)
        print(result)

world_1()
