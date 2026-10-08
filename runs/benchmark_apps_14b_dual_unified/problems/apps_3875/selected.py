import sys
from fractions import Fraction

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    MOD = 1000000007
    
    def count_sequences(A):
        total_sequences = 1
        for a in A:
            total_sequences *= a
        return total_sequences
    
    def dp_lis_length(A):
        n = len(A)
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = 1
            for j in range(1, i):
                if A[j-1] < A[i-1]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return dp[n]
    
    total_sequences = count_sequences(A)
    total_lis_length = 0
    
    from itertools import product
    
    for seq in product(*(range(1, a+1) for a in A)):
        lis_length = dp_lis_length(seq)
        total_lis_length += lis_length
    
    expected_value = Fraction(total_lis_length, total_sequences)
    result = expected_value.numerator * pow(expected_value.denominator, -1, MOD) % MOD
    
    print(result)

if __name__ == "__main__":
    main()