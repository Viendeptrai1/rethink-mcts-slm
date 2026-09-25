import sys

def max_substring_to_remove(s, t):
    n, m = len(s), len(t)
    
    # Create a DP table to store the indices of matching characters
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Find the maximum length of the substring to remove
    max_length = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if dp[i][j] == m:
                # Calculate the length of the substring to remove
                length = i + (n - j)
                max_length = max(max_length, length)
    
    return max_length

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Output the result
print(max_substring_to_remove(s, t))