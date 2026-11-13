def generate_integers(a, b):
    start = min(a, b)
    end = max(a, b)
    return [i for i in range(start, end + 1) if i % 2 == 0]