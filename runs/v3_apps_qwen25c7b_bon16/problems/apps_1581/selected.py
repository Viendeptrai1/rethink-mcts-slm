import sys
from functools import lru_cache

MOD = 10**9 + 7

def count_sequences(N, K):
    @lru_cache(None)
    def dp(i, last):
        if i == K:
            return 1
        count = 0
        for next_num in range(1, N // last + 1):
            count += dp(i + 1, next_num)
        return count % MOD

    total_sequences = 0
    for num in range(1, N + 1):
        total_sequences += dp(1, num)
    return total_sequences % MOD

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    print(count_sequences(N, K))