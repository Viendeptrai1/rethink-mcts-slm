def max_equal_sum_split(n, d):
    total_sum = sum(d)
    if total_sum % 2 != 0:
        return 0
    
    target_sum = total_sum // 2
    dp = [-float('inf')] * (target_sum + 1)
    dp[0] = 0
    
    for num in d:
        for j in range(target_sum, num - 1, -1):
            dp[j] = max(dp[j], dp[j - num] + num)
    
    return dp[target_sum]

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
d = list(map(int, data[1:]))

# Output the result
print(max_equal_sum_split(n, d))