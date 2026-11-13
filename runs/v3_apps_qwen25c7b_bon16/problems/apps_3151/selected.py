import sys

def find_square_tiles(n):
    for m in range(1, int(n**0.5) + 2):
        k_squared = m**2 - n
        k = int(k_squared**0.5)
        if k * k == k_squared:
            return m, k
    return "impossible"

input_line = sys.stdin.read().strip()
n = int(input_line)
print(find_square_tiles(n))