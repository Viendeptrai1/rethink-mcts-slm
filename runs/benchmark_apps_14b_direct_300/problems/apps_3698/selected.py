MOD = 10**9 + 7

def count_special_numbers(n, k):
    def count_ones(x):
        return bin(x).count('1')
    
    def dp(n, k):
        if n == 0:
            return 0
        if k == 0:
            return 1 if count_ones(n) == 1 else 0
        
        ans = 0
        for i in range(n.bit_length()):
            if n & (1 << i):
                ans += dp(n ^ (1 << i), k - 1)
                ans %= MOD
        return ans
    
    return dp(int(n, 2), k)

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = data[0]
k = int(data[1])

# Output the result
print(count_special_numbers(n, k))