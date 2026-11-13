from sys import stdin, stdout
from functools import lru_cache
import math

def mod_inv(a, m):
    return pow(a, m - 2, m)

@lru_cache(None)
def catalan(n, mod):
    if n == 0 or n == 1:
        return 1
    c = 0
    for i in range(0, n + 1):
        c += catalan(i, mod) * catalan(n - i, mod)
        c %= mod
    return c

@lru_cache(None)
def count_permutations(n, k, mod):
    if n == 1:
        return 1
    result = 0
    for i in range(1, min(k, n) + 1):
        result += count_permutations(n - i, i, mod) * catalan(i, mod)
        result %= mod
    return result

def main():
    input = stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    p = int(data[2])

    result = count_permutations(n, k, p)
    stdout.write(str(result))

if __name__ == "__main__":
    main()