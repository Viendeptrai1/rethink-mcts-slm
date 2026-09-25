import sys

def max_increasing_subarray_length(n, a):
    # Arrays to store the length of the longest increasing subarray ending at each index
    # and starting at each index
    end_here = [1] * n
    start_here = [1] * n
    
    # Fill end_here array
    for i in range(1, n):
        if a[i] > a[i - 1]:
            end_here[i] = end_here[i - 1] + 1
    
    # Fill start_here array
    for i in range(n - 2, -1, -1):
        if a[i] < a[i + 1]:
            start_here[i] = start_here[i + 1] + 1
    
    # Calculate the maximum length of the increasing subarray after removing at most one element
    max_length = 0
    for i in range(n):
        # If we remove the element at index i
        if i == 0:
            max_length = max(max_length, start_here[i + 1])
        elif i == n - 1:
            max_length = max(max_length, end_here[i - 1])
        else:
            max_length = max(max_length, end_here[i - 1] + start_here[i + 1])
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(max_increasing_subarray_length(n, a))