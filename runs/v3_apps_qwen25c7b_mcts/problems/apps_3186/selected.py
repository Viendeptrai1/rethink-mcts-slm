from math import comb

def count_ways(N, M, K):
    MOD = 10**6 + 7
    return comb(N + M - 1, K) % MOD

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