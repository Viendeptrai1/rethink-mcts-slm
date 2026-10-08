MOD = 10**9 + 7

def count_special_numbers(n, k):
    # Convert n from binary string to integer
    n = int(n, 2)
    
    # Initialize DP table
    dp = [[0] * (k + 1) for _ in range(1001)]
    dp[0][0] = 1
    
    # Fill DP table
    for i in range(1, 1001):
        for j in range(k + 1):
            dp[i][j] = dp[i - 1][j]
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i - 1][j - 1]) % MOD
    
    # Count numbers with exactly k operations to reduce to 1
    def count_operations(x, operations):
        if x == 0:
            return 1 if operations == 0 else 0
        if operations < 0:
            return 0
        count = 0
        while x > 0:
            if x & 1:
                count += count_operations(x ^ 1, operations - 1)
                count %= MOD
            x >>= 1
        return count
    
    # Calculate the result
    result = 0
    for i in range(1, n + 1):
        if bin(i).count('1') == 1:
            continue
        result = (result + count_operations(i, k)) % MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = data[0]
k = int(data[1])

# Output the result
print(count_special_numbers(n, k))