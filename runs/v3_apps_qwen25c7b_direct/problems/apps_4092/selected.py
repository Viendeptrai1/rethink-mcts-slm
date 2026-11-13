def min_insertions_to_avoid_zero_sum_subarrays(n, arr):
    # Initialize variables
    count = 0
    current_sum = 0
    
    # Iterate through the array
    for num in arr:
        current_sum += num
        if current_sum == 0:
            count += 1
            current_sum = 0
    
    return count

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
arr = list(map(int, data[1:]))

# Output the result
print(min_insertions_to_avoid_zero_sum_subarrays(n, arr))