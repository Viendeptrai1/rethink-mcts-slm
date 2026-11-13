def count_unsorted_permutations(n, a):
    MOD = 10**9 + 9

    # Helper function to compute factorial modulo MOD
    def factorial_mod(x, mod):
        result = 1
        for i in range(2, x + 1):
            result = (result * i) % mod
        return result

    # Helper function to compute inverse of a number using Fermat's Little Theorem
    def mod_inverse(x, mod):
        return pow(x, mod - 2, mod)

    # Count frequencies of each number
    from collections import Counter
    frequency = Counter(a)

    # Calculate factorial of n
    fact_n = factorial_mod(n, MOD)

    # Calculate the denominator: product of factorials of frequencies
    denom = 1
    for count in frequency.values():
        denom = (denom * factorial_mod(count, MOD)) % MOD

    # Calculate the number of permutations of the entire sequence
    total_permutations = fact_n

    # Calculate the number of sorted permutations
    sorted_permutations = denom

    # Number of unsorted permutations is the difference
    unsorted_permutations = (total_permutations - sorted_permutations + MOD) % MOD

    return unsorted_permutations

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

print(count_unsorted_permutations(n, a))