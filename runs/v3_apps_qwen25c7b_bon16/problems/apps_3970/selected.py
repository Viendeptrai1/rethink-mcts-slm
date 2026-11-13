def largest_k_multiple_free_subset_size(n, k, nums):
    nums.sort()
    dp = [1] * n
    max_size = 1
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] % nums[j] == 0 and nums[i] // nums[j] == k:
                break
        else:
            dp[i] = dp[j] + 1
            max_size = max(max_size, dp[i])
    
    return max_size

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
nums = list(map(int, data[2:]))

# Output the result
print(largest_k_multiple_free_subset_size(n, k, nums))