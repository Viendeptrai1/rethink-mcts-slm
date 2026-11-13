import sys
from fractions import Fraction
from math import gcd

MOD = 1000000007

def expected_lis_length(N, A):
    def lis_length(sequence):
        if not sequence:
            return 0
        dp = [1] * len(sequence)
        for i in range(1, len(sequence)):
            for j in range(i):
                if sequence[i] > sequence[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)

    def generate_sequences(index, current_sequence):
        if index == N:
            yield current_sequence
            return
        for x in range(1, A[index] + 1):
            yield from generate_sequences(index + 1, current_sequence + [x])

    total_lis_length = 0
    total_sequences = 0

    for sequence in generate_sequences(0, []):
        total_lis_length += lis_length(sequence)
        total_sequences += 1

    expected_value = Fraction(total_lis_length, total_sequences)
    P = expected_value.numerator
    Q = expected_value.denominator

    g = gcd(P, Q)
    P //= g
    Q //= g

    R = (P * pow(Q, MOD - 2, MOD)) % MOD
    return R

def main():
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    A = list(map(int, data[1:]))
    result = expected_lis_length(N, A)
    print(result)

if __name__ == "__main__":
    main()