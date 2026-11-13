def find_remaining_marks(n, k, p, x, y, a):
    from itertools import product

    # Calculate the current sum and the number of marks needed
    current_sum = sum(a)
    remaining_tests = n - k

    # Calculate the possible range for the remaining marks
    min_remaining_sum = max(0, x - current_sum)
    max_remaining_sum = (n - k) * p

    # Generate all possible combinations of remaining marks
    possible_remaining_marks = product(range(1, p + 1), repeat=remaining_tests)

    for remaining in possible_remaining_marks:
        total_sum = current_sum + sum(remaining)
        if total_sum > x:
            continue

        # Sort the current marks and the remaining marks to calculate the median
        all_marks = sorted(a + list(remaining))
        median_index = (n + 1) // 2
        median = all_marks[median_index - 1]

        if median >= y:
            return remaining

    return -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
p = int(data[2])
x = int(data[3])
y = int(data[4])
a = list(map(int, data[5:5 + k]))

# Get the result and print it
result = find_remaining_marks(n, k, p, x, y, a)
if result == -1:
    print(result)
else:
    print(" ".join(map(str, result)))