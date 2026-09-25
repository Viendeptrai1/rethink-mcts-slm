import sys

def max_substring_to_remove(s, t):
    n, m = len(s), len(t)
    # Create a list to store the last occurrence of each character in t
    last_occurrence = [-1] * 26
    for i in range(m):
        last_occurrence[ord(t[i]) - ord('a')] = i
    
    # Initialize the DP table
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(m + 1):
            if j == 0:
                dp[i][j] = 1
            elif s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = dp[i - 1][j]
    
    # Find the maximum length of the substring to remove
    max_length = 0
    for i in range(1, n + 1):
        for j in range(m + 1):
            if dp[i][j] == j:
                max_length = max(max_length, i - j)
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
s = data[0]
t = data[1]

# Calculate and print the result
result = max_substring_to_remove(s, t)
print(result)