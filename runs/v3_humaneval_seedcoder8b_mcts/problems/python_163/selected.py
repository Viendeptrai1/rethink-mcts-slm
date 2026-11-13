def generate_integers(a, b):
    return sorted([x for x in range(0, 10, 2) if min(a, b) <= x <= max(a, b)])