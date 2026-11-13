def max_sum_partition(n, d):
    # Calculate prefix sums
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + d[i]

    # Calculate suffix sums
    suffix_sum = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + d[i]

    # Initialize the maximum sum
    max_sum = 0

    # Iterate over all possible partition points
    for i in range(n + 1):
        for j in range(i, n + 1):
            sum1 = prefix_sum[i]
            sum3 = suffix_sum[j]
            if sum1 == sum3:
                max_sum = max(max_sum, sum1)

    return max_sum

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
d = list(map(int, data[1:n+1]))

# Get the result and print it
result = max_sum_partition(n, d)
print(result)