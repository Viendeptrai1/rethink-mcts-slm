def min_insertions_to_avoid_zero_sum_subarray(n, array):
    # Initialize prefix sum and a set to track prefix sums
    prefix_sum = 0
    prefix_sums = set()
    prefix_sums.add(0)  # To handle the case where a prefix itself is zero
    insertions = 0

    for num in array:
        prefix_sum += num
        if prefix_sum in prefix_sums:
            # If the prefix sum has been seen before, we need an insertion
            insertions += 1
            # Reset the prefix sum to avoid zero sum subarray
            prefix_sum = 0
            # Clear the set and add the new prefix sum
            prefix_sums = {0}
        else:
            prefix_sums.add(prefix_sum)

    return insertions

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
array = list(map(int, data[1:n+1]))

# Get the result and print it
result = min_insertions_to_avoid_zero_sum_subarray(n, array)
print(result)