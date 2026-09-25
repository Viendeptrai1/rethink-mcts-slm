import sys

def max_increasing_subarray_length(n, a):
    # Initialize variables to store the maximum length of increasing subarrays
    max_len = 0
    current_len = 1
    
    # Find the longest increasing subarray without any removal
    for i in range(1, n):
        if a[i] > a[i - 1]:
            current_len += 1
        else:
            max_len = max(max_len, current_len)
            current_len = 1
    max_len = max(max_len, current_len)
    
    # Check if removing any single element can extend the longest subarray
    for i in range(n):
        left_len = 0
        right_len = 0
        
        # Calculate the length of the increasing subarray to the left of a[i]
        for j in range(i - 1, -1, -1):
            if a[j] < a[j + 1]:
                left_len += 1
            else:
                break
        
        # Calculate the length of the increasing subarray to the right of a[i]
        for j in range(i + 1, n):
            if a[j] > a[j - 1]:
                right_len += 1
            else:
                break
        
        # Update the maximum length considering the removal of a[i]
        max_len = max(max_len, left_len + right_len + 1)
    
    return max_len

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Calculate and print the result
result = max_increasing_subarray_length(n, a)
print(result)