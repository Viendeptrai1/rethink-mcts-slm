import sys

def find_square_sides(n):
    for m in range(1, int(n**0.5) + 1):
        k_squared = m**2 - n
        k = int(k_squared**0.5)
        if k * k == k_squared:
            return m, k
    return "impossible"

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    result = find_square_sides(n)
    print(result)