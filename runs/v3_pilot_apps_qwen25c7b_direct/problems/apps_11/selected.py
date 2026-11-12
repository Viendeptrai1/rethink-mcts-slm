def max_chocolates(n, a, b, p, q):
    red_tiles = n // a + n // b - n // (a * b)
    blue_tiles = n // b + n // a - n // (a * b)
    return max(red_tiles * p, blue_tiles * q)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = list(map(int, input().split()))
    n, a, b, p, q = data[0], data[1], data[2], data[3], data[4]
    result = max_chocolates(n, a, b, p, q)
    print(result)