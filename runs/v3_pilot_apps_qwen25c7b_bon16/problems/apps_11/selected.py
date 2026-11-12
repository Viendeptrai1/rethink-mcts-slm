def max_chocolates(n, a, b, p, q):
    lcm = (a * b) // gcd(a, b)
    red_tiles = n // a + n // b - n // lcm
    blue_tiles = n // b - n // lcm
    total_chocolates = red_tiles * p + blue_tiles * q
    return total_chocolates

from math import gcd

# Example usage:
n, a, b, p, q = map(int, input().split())
print(max_chocolates(n, a, b, p, q))