import sys
from functools import lru_cache

def count_permutations(n, k, p):
    @lru_cache(None)
    def dp(i, j, up):
        if i == n:
            return 1
        res = 0
        if up:
            for x in range(j + 1, min(n, j + k) + 1):
                res = (res + dp(i + 1, x, True)) % p
            if j + k <= n:
                res = (res + dp(i + 1, j + k, False)) % p
        else:
            for x in range(max(1, j - k), j):
                res = (res + dp(i + 1, x, False)) % p
            if j - k >= 1:
                res = (res + dp(i + 1, j - k, True)) % p
        return res

    return (dp(1, 1, True) + dp(1, 1, False)) % p

if __name__ == "__main__":
    n, k, p = map(int, sys.stdin.read().split())
    print(count_permutations(n, k, p))