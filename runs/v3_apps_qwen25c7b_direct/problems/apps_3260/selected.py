from math import factorial

def count_permutations(n, k, p):
    def mod_inv(a, p):
        return pow(a, p - 2, p)
    
    def catalan_number(n, p):
        c = [0] * (n + 1)
        c[0] = 1
        for i in range(1, n + 1):
            c[i] = ((2 * (2 * i - 1) * c[i - 1]) % p + p) % p
        return c[n]
    
    def stirling_second_kind(n, k, p):
        s = [[0] * (k + 1) for _ in range(n + 1)]
        s[0][0] = 1
        for i in range(1, n + 1):
            for j in range(1, min(i, k) + 1):
                s[i][j] = ((i - 1) * s[i - 1][j] + s[i - 1][j - 1]) % p
        return s[n][k]
    
    def multinomial_coefficient(arr, p):
        num = factorial(sum(arr)) % p
        den = 1
        for x in arr:
            den = (den * factorial(x)) % p
        return (num * mod_inv(den, p)) % p
    
    total_permutations = factorial(n) % p
    valid_permutations = 0
    for r in range(1, k + 1):
        valid_permutations += stirling_second_kind(n, r, p) * catalan_number(r, p) % p
    valid_permutations %= p
    
    result = (total_permutations - valid_permutations + p) % p
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
p = int(data[2])

# Calculate and print the result
print(count_permutations(n, k, p))