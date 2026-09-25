import sys

def longest_increasing_subsequence(n, a):
    # Initialize DP arrays
    dp_left = [1] * n
    dp_right = [1] * n
    
    # Fill dp_left array
    for i in range(1, n):
        if a[i] > a[i - 1]:
            dp_left[i] = dp_left[i - 1] + 1
    
    # Fill dp_right array
    for i in range(n - 2, -1, -1):
        if a[i] < a[i + 1]:
            dp_right[i] = dp_right[i + 1] + 1
    
    # Find the maximum length of the increasing subsequence
    max_length = 0
    for i in range(n):
        max_length = max(max_length, dp_left[i] + dp_right[i] - 1)
    
    # Reconstruct the sequence
    result = []
    left = 0
    right = n - 1
    while left <= right:
        if dp_left[left] >= dp_right[right]:
            result.append('L')
            left += 1
        else:
            result.append('R')
            right -= 1
    
    return max_length, ''.join(result)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Get the result
k, s = longest_increasing_subsequence(n, a)

# Print the result
print(k)
print(s)