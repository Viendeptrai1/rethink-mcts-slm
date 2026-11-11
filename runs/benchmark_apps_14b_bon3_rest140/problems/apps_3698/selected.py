MOD = 10**9 + 7

def count_special_numbers(n, k):
    def count_bits(x):
        return bin(x).count('1')
    
    def dp(i, j, tight):
        if i == len(n):
            return j == 0
        if (i, j, tight) in memo:
            return memo[(i, j, tight)]
        
        limit = int(n[i]) if tight else 1
        result = 0
        for digit in range(limit + 1):
            new_tight = tight and digit == limit
            new_j = j - (digit == 1)
            if new_j >= 0:
                result = (result + dp(i + 1, new_j, new_tight)) % MOD
        
        memo[(i, j, tight)] = result
        return result
    
    memo = {}
    return dp(0, k, True)

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = data[0]
k = int(data[1])

# Output the result
print(count_special_numbers(n, k))