def min_insertions_to_avoid_zero_sum_subarray(n, array):
    from collections import defaultdict

    prefix_sum = 0
    prefix_count = defaultdict(int)
    prefix_count[0] = 1  # To handle the case where a prefix sum itself is zero
    insertions = 0

    for num in array:
        prefix_sum += num
        if prefix_count[prefix_sum] > 0:
            # If the current prefix sum has been seen before,
            # it means there is a zero-sum subarray ending here.
            insertions += 1
            # Reset the prefix sum count to avoid counting the same zero-sum subarray again
            prefix_count.clear()
            prefix_count[0] = 1
            prefix_sum = num
        prefix_count[prefix_sum] += 1

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