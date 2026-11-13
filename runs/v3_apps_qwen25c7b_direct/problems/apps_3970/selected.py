def largest_k_multiple_free_subset(n, k, arr):
    arr.sort()
    dp = [1] * n
    max_size = 1
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] % arr[j] == 0 and arr[i] // arr[j] == k:
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
arr = list(map(int, data[2:]))

# Output the result
print(largest_k_multiple_free_subset(n, k, arr))