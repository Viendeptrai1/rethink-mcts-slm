import sys
from math import comb

MOD = 10**6 + 7

def solve(N, M, K):
    if K > N * M:
        return 0
    return comb(N * M, K) % MOD

def main():
    input_data = sys.stdin.read().strip()
    N, M, K = map(int, input_data.split())
    result = solve(N, M, K)
    print(result)

if __name__ == "__main__":
    main()