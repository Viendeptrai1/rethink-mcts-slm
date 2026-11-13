def min_insertions_to_avoid_zero_sum_subsegments(n, a):
    prefix_sums = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sums[i] = prefix_sums[i - 1] + a[i - 1]

    seen_prefix_sums = set()
    count = 0

    for prefix_sum in prefix_sums:
        if prefix_sum in seen_prefix_sums:
            count += 1
            seen_prefix_sums.clear()
        seen_prefix_sums.add(prefix_sum)

    return count

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

print(min_insertions_to_avoid_zero_sum_subsegments(n, a))