import sys

def max_increasing_subarray_length(n, a):
    # Initialize variables to store the lengths of the longest increasing subarrays
    left_lengths = [1] * n
    right_lengths = [1] * n
    
    # Calculate the lengths of the longest increasing subarrays ending at each position
    for i in range(1, n):
        if a[i] > a[i - 1]:
            left_lengths[i] = left_lengths[i - 1] + 1
    
    # Calculate the lengths of the longest increasing subarrays starting at each position
    for i in range(n - 2, -1, -1):
        if a[i] < a[i + 1]:
            right_lengths[i] = right_lengths[i + 1] + 1
    
    # Calculate the maximum length of the increasing subarray after removing at most one element
    max_length = 0
    for i in range(n):
        # Case 1: Remove the element at position i
        max_length = max(max_length, max(left_lengths[i - 1] if i > 0 else 0, right_lengths[i + 1] if i < n - 1 else 0))
        # Case 2: Merge the increasing subarrays on both sides of the element at position i
        if i > 0 and i < n - 1 and a[i - 1] < a[i + 1]:
            max_length = max(max_length, left_lengths[i - 1] + right_lengths[i + 1])
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Calculate and print the result
result = max_increasing_subarray_length(n, a)
print(result)