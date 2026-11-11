import sys
from fractions import Fraction

MOD = 1000000007

def expected_lis_length(N, A):
    total_cases = 1
    for a in A:
        total_cases *= a
        total_cases %= MOD

    dp = [[Fraction(0) for _ in range(N + 1)] for _ in range(N + 1)]
    dp[0][0] = Fraction(1)

    for i in range(1, N + 1):
        for j in range(i + 1):
            dp[i][j] = dp[i - 1][j]
            if j > 0:
                dp[i][j] += dp[i - 1][j - 1] * Fraction(1, A[i - 1])
            dp[i][j] %= MOD

    expected_value = sum(dp[N][j] * j for j in range(N + 1))
    expected_value %= MOD

    return int(expected_value)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    result = expected_lis_length(N, A)
    print(result)

if __name__ == "__main__":
    main()