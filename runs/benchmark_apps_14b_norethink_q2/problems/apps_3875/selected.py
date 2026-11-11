import sys
from itertools import product
from fractions import Fraction

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    MOD = 1000000007
    
    def lis_length(seq):
        if not seq:
            return 0
        dp = [1] * len(seq)
        for i in range(1, len(seq)):
            for j in range(i):
                if seq[i] > seq[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
    
    total_sequences = 1
    for a in A:
        total_sequences *= a
    
    total_lis_length = 0
    
    for seq in product(*(range(1, a + 1) for a in A)):
        total_lis_length += lis_length(seq)
    
    expected_value = Fraction(total_lis_length, total_sequences)
    result = expected_value.numerator * pow(expected_value.denominator, -1, MOD) % MOD
    
    print(result)

if __name__ == "__main__":
    main()