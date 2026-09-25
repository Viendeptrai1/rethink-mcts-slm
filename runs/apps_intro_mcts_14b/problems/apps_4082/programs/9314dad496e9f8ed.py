import sys

def max_increasing_subarray_length(n, a):
    # Initialize variables to store the maximum length of increasing subarrays
    max_length = 0
    current_length = 1
    
    # Arrays to store the length of increasing subarray ending at each index
    left_lengths = [1] * n
    right_lengths = [1] * n
    
    # Calculate left lengths
    for i in range(1, n):
        if a[i] > a[i - 1]:
            left_lengths[i] = left_lengths[i - 1] + 1
    
    # Calculate right lengths
    for i in range(n - 2, -1, -1):
        if a[i] < a[i + 1]:
            right_lengths[i] = right_lengths[i + 1] + 1
    
    # Calculate the maximum length by considering removal of each element
    for i in range(n):
        if i == 0:
            max_length = max(max_length, right_lengths[i + 1])
        elif i == n - 1:
            max_length = max(max_length, left_lengths[i - 1])
        else:
            max_length = max(max_length, left_lengths[i - 1] + right_lengths[i + 1])
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(max_increasing_subarray_length(n, a))