import sys
from fractions import Fraction

def expected_length_of_lis(N, A):
    MOD = 1000000007
    dp = [Fraction(1)] * (N + 1)
    
    for i in range(1, N + 1):
        new_dp = [Fraction(0)] * (i + 1)
        for j in range(i):
            new_dp[j] += dp[j] * Fraction(j + 1, A[i - 1])
            new_dp[j + 1] += dp[j] * Fraction(A[i - 1] - j, A[i - 1])
        dp = new_dp
    
    return int(dp[-1].numerator * pow(dp[-1].denominator, MOD - 2, MOD)) % MOD

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    A = list(map(int, data[1:]))
    result = expected_length_of_lis(N, A)
    print(result)