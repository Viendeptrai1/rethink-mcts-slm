def min_insertions_to_avoid_zero_sum_subarray(n, arr):
    prefix_sum = 0
    seen_sums = {0: -1}  # Maps prefix sum to its last index
    insertions_needed = 0

    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum in seen_sums:
            # If we've seen this prefix sum before, it means we have a zero sum subarray
            insertions_needed += 1
            # Reset prefix sum and seen_sums except for the last occurrence of the current prefix sum
            prefix_sum = arr[i]
            seen_sums = {0: -1, prefix_sum: i}
        else:
            seen_sums[prefix_sum] = i

    return insertions_needed

# Reading input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
arr = list(map(int, data[1:n+1]))

# Calculating and printing the result
result = min_insertions_to_avoid_zero_sum_subarray(n, arr)
print(result)