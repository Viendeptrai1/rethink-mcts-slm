import sys

def max_removable_substring(s, t):
    m, n = len(s), len(t)
    
    # dp[i][j] will store the farthest position in t that can be matched up to position i in s
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill the dp table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = dp[i - 1][j]
    
    # Now, we need to find the maximum length of the substring we can remove
    max_length = 0
    
    # Check each possible substring in s
    for l in range(m):
        for r in range(l, m):
            # Check if t is still a subsequence of s after removing s[l:r+1]
            if dp[l][n] + dp[m][n] - dp[r + 1][n] == n:
                max_length = max(max_length, r - l + 1)
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
s = data[0]
t = data[1]

# Output the result
print(max_removable_substring(s, t))