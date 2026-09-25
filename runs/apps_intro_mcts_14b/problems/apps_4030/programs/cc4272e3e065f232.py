import sys

def min_colors_to_sort(s):
    n = len(s)
    if n == 1:
        return 1, [1]
    
    # Initialize the dp array where dp[i] is the length of the longest increasing subsequence ending at s[i]
    dp = [1] * n
    
    # Fill the dp array
    for i in range(1, n):
        for j in range(i):
            if s[i] >= s[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    # The minimum number of colors needed is the maximum value in the dp array
    res = max(dp)
    
    # Now we need to construct the coloring
    color = [0] * n
    current_color = 1
    
    # We will fill the color array from right to left
    for i in range(n-1, -1, -1):
        if dp[i] == res:
            color[i] = current_color
            res -= 1
        else:
            for j in range(i-1, -1, -1):
                if dp[j] == dp[i] + 1 and s[j] < s[i]:
                    color[i] = color[j]
                    break
    
    return res + 1, color

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Get the result
res, color = min_colors_to_sort(s)

# Print the result
print(res)
print(' '.join(map(str, color)))