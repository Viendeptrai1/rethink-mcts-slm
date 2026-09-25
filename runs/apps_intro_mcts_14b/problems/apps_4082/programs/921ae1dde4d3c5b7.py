import sys

def max_increasing_subarray_length(n, a):
    if n == 1:
        return 1
    
    # Initialize variables to keep track of the longest increasing subarrays
    left_lengths = [1] * n
    right_lengths = [1] * n
    
    # Calculate lengths of increasing subarrays ending at each position
    for i in range(1, n):
        if a[i] > a[i - 1]:
            left_lengths[i] = left_lengths[i - 1] + 1
    
    # Calculate lengths of increasing subarrays starting at each position
    for i in range(n - 2, -1, -1):
        if a[i] < a[i + 1]:
            right_lengths[i] = right_lengths[i + 1] + 1
    
    # Calculate the maximum length of the increasing subarray after removing one element
    max_length = 0
    
    # Case 1: Remove the first element
    max_length = max(max_length, right_lengths[1])
    
    # Case 2: Remove the last element
    max_length = max(max_length, left_lengths[n - 2])
    
    # Case 3: Remove an element between the first and last
    for i in range(1, n - 1):
        if a[i - 1] < a[i + 1]:
            max_length = max(max_length, left_lengths[i - 1] + right_lengths[i + 1])
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(max_increasing_subarray_length(n, a))