import sys
from fractions import Fraction
from functools import lru_cache

MOD = 1000000007

def mod_inverse(a, m):
    """ Returns the modular inverse of a under modulo m """
    return pow(a, m - 2, m)

def expected_value_of_longest_increasing_subsequence(N, A):
    @lru_cache(None)
    def lis_length(sequence):
        """ Computes the length of the longest increasing subsequence """
        if not sequence:
            return 0
        dp = [1] * len(sequence)
        for i in range(1, len(sequence)):
            for j in range(i):
                if sequence[i] > sequence[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)

    def generate_sequences(index, current_sequence):
        """ Generates all possible sequences recursively """
        if index == N:
            yield tuple(current_sequence)
        else:
            for x in range(1, A[index] + 1):
                yield from generate_sequences(index + 1, current_sequence + [x])

    total_length = 0
    total_count = 0

    for seq in generate_sequences(0, []):
        total_length += lis_length(seq)
        total_count += 1

    fraction = Fraction(total_length, total_count)
    P = fraction.numerator
    Q = fraction.denominator

    # We need to find R such that R * Q ≡ P (mod MOD)
    R = (P * mod_inverse(Q, MOD)) % MOD

    return R

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    result = expected_value_of_longest_increasing_subsequence(N, A)
    print(result)

if __name__ == "__main__":
    main()