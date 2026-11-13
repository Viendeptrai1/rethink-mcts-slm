def generate_integers(a, b):
    start, end = min(a, b), max(a, b)
    return sorted([i for i in range(start, end + 1) if i % 2 == 0 and i % 10 in [0, 2, 4, 6, 8]])