def generate_integers(a, b):
    if a > b:
        a, b = b, a
    return [x for x in range(a, b + 1) if x % 2 == 0]