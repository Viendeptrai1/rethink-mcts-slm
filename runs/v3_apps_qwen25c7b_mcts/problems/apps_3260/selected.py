from functools import lru_cache

@lru_cache(None)
def count_permutations(n, k, p):
    if n == 0:
        return 1
    total = 0
    for i in range(1, min(k, n) + 1):
        total += count_permutations(n - i, k, p) * factorial(i) % p
    return total % p

@lru_cache(None)
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    p = int(data[2])
    result = count_permutations(n, k, p)
    print(result)

if __name__ == "__main__":
    main()