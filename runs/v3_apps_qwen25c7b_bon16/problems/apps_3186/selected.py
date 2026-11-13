from math import comb

def count_ways(N, M, K):
    MOD = 10**6 + 7
    total_ways = 0
    for i in range(min(K, N * M) + 1):
        if (K - i) % M == 0:
            ways_to_choose = comb(N, i)
            total_ways = (total_ways + ways_to_choose) % MOD
    return total_ways

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    print(count_ways(N, M, K))