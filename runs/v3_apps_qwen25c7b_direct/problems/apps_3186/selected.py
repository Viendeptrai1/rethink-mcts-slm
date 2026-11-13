from math import comb

def count_ways(N, M, K):
    MOD = 10**6 + 7
    total_ways = 0
    for i in range(min(K, N) + 1):
        if (K - i) % M == 0:
            total_ways += comb(N, i)
            total_ways %= MOD
    return total_ways

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    result = count_ways(N, M, K)
    print(result)