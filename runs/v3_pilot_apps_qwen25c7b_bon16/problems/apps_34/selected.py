def max_pieces(n, a, b):
    return min((a + b - 1) // n, min(a, b))

# Read input
n, a, b = map(int, input().split())

# Output result
print(max_pieces(n, a, b))