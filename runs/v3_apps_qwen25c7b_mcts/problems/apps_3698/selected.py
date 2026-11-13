MOD = 10**9 + 7

def count_special_numbers(n, k):
    # Convert n to binary and remove the '0b' prefix
    binary_n = bin(int(n, 2))[2:]
    
    # Initialize dp array
    dp = [0] * (k + 1)
    dp[0] = 1
    
    # Iterate through each bit position
    for i in range(len(binary_n)):
        new_dp = [0] * (k + 1)
        for j in range(min(i + 1, k + 1)):
            new_dp[j] = dp[j]
            if j > 0:
                new_dp[j] += dp[j - 1]
                new_dp[j] %= MOD
        dp = new_dp
    
    return dp[k]

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = data[0]
k = int(data[1])

# Output the result
print(count_special_numbers(n, k))