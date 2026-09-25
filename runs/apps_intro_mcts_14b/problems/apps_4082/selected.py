import sys

def max_increasing_subarray_length(n, a):
    # Find all increasing subarrays
    increasing_lengths = []
    current_length = 1
    
    for i in range(1, n):
        if a[i] > a[i - 1]:
            current_length += 1
        else:
            increasing_lengths.append(current_length)
            current_length = 1
    increasing_lengths.append(current_length)
    
    # If the entire array is increasing
    if len(increasing_lengths) == 1:
        return n
    
    # Calculate the maximum length after removing one element
    max_length = 0
    for i in range(len(increasing_lengths)):
        if i == 0:
            # Remove from the start
            max_length = max(max_length, increasing_lengths[i + 1])
        elif i == len(increasing_lengths) - 1:
            # Remove from the end
            max_length = max(max_length, increasing_lengths[i - 1])
        else:
            # Remove from the middle
            max_length = max(max_length, increasing_lengths[i - 1] + increasing_lengths[i + 1])
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(max_increasing_subarray_length(n, a))