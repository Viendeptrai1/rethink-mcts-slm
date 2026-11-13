def generate_integers(a, b):
    start = min(a, b)
    end = max(a, b)
    return [num for num in range(start, end + 1) if num % 2 == 0]