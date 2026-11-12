def distances_to_nearest_zero(n, arr):
    left_dist = [float('inf')] * n
    right_dist = [float('inf')] * n
    
    # Calculate distances from left to right
    last_zero = -1
    for i in range(n):
        if arr[i] == 0:
            last_zero = i
        if last_zero != -1:
            left_dist[i] = i - last_zero
    
    # Calculate distances from right to left
    last_zero = -1
    for i in range(n-1, -1, -1):
        if arr[i] == 0:
            last_zero = i
        if last_zero != -1:
            right_dist[i] = last_zero - i
    
    # Combine the results
    result = []
    for i in range(n):
        result.append(min(left_dist[i], right_dist[i]))
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
arr = list(map(int, data[1:]))

# Get the result
result = distances_to_nearest_zero(n, arr)

# Print the result
print(" ".join(map(str, result)))