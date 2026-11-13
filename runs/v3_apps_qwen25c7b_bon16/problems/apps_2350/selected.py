from math import comb

def count_possible_sums(x1, y1, x2, y2):
    # Calculate the total number of steps to reach (x2, y2)
    total_steps = (x2 - x1) + (y2 - y1)
    # Calculate the minimum and maximum possible sums
    min_sum = (x1 * (x1 + 1)) // 2 + (y1 * (y1 + 1)) // 2
    max_sum = (x2 * (x2 + 1)) // 2 + (y2 * (y2 + 1)) // 2
    # If the minimum and maximum sums are the same, there's only one possible sum
    if min_sum == max_sum:
        return 1
    # Otherwise, the number of possible sums is the number of ways to choose
    # (total_steps - (x2 - x1)) positions out of total_steps for the right moves
    else:
        return comb(total_steps, total_steps - (x2 - x1))

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Process each test case
results = []
index = 1
for _ in range(int(data[0])):
    x1 = int(data[index])
    y1 = int(data[index + 1])
    x2 = int(data[index + 2])
    y2 = int(data[index + 3])
    index += 4
    results.append(count_possible_sums(x1, y1, x2, y2))

# Output results
print("\n".join(map(str, results)))