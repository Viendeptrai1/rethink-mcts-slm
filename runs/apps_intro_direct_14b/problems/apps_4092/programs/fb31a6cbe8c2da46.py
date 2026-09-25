import sys

def min_insertions_to_avoid_zero_sum_subarray(n, a):
    # We will use a set to keep track of prefix sums
    prefix_sums = set()
    current_sum = 0
    insertions = 0

    for i in range(n):
        current_sum += a[i]
        if current_sum in prefix_sums:
            # If we encounter a prefix sum that we've seen before,
            # it means there's a subarray with sum 0.
            # We need to insert an element to break this.
            insertions += 1
            # Reset the prefix sums set and current sum
            prefix_sums = {current_sum}
            current_sum = a[i]
        else:
            prefix_sums.add(current_sum)

    return insertions

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Calculate and print the result
result = min_insertions_to_avoid_zero_sum_subarray(n, a)
print(result)