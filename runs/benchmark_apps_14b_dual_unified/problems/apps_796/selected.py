import sys
from math import comb

MOD = 10**9 + 7

def count_ways(n, k):
    if n == 1:
        return k
    total_ways = pow(k, n * n, MOD)
    for i in range(1, n):
        total_ways -= comb(n, i) * pow(k - 1, n * n - i * n, MOD)
        total_ways %= MOD
    return total_ways

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    print(count_ways(n, k))

if __name__ == "__main__":
    main()