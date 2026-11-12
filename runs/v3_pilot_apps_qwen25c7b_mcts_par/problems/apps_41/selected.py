import sys

def min_distance_to_zero(n, arr):
    prefix = [float('inf')] * n
    suffix = [float('inf')] * n
    
    # Calculate prefix distances
    last_zero = -1
    for i in range(n):
        if arr[i] == 0:
            last_zero = i
        if last_zero != -1:
            prefix[i] = i - last_zero
    
    # Calculate suffix distances
    last_zero = -1
    for i in range(n-1, -1, -1):
        if arr[i] == 0:
            last_zero = i
        if last_zero != -1:
            suffix[i] = last_zero - i
    
    # Combine prefix and suffix distances
    result = []
    for i in range(n):
        result.append(min(prefix[i], suffix[i]))
    
    return result

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
arr = list(map(int, data[1:]))

# Get the result
result = min_distance_to_zero(n, arr)

# Print the result
print(" ".join(map(str, result)))