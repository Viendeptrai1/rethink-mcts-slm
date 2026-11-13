def max_significance(n, m, d, physics_cups, informatics_cups):
    # Sort cups by significance in descending order
    physics_cups.sort(reverse=True, key=lambda x: x[0])
    informatics_cups.sort(reverse=True, key=lambda x: x[0])

    # Compute prefix sums for both subjects
    physics_prefix = [(0, 0)]  # (total_significance, total_width)
    informatics_prefix = [(0, 0)]

    for c, w in physics_cups:
        total_significance = physics_prefix[-1][0] + c
        total_width = physics_prefix[-1][1] + w
        physics_prefix.append((total_significance, total_width))

    for c, w in informatics_cups:
        total_significance = informatics_prefix[-1][0] + c
        total_width = informatics_prefix[-1][1] + w
        informatics_prefix.append((total_significance, total_width))

    max_total_significance = 0

    # Try all combinations of exposing at least one cup from each subject
    for i in range(1, len(physics_prefix)):
        if physics_prefix[i][1] > d:
            break
        remaining_width = d - physics_prefix[i][1]

        # Binary search for the maximum significance we can get from informatics
        low, high = 0, len(informatics_prefix) - 1
        while low <= high:
            mid = (low + high) // 2
            if informatics_prefix[mid][1] <= remaining_width:
                low = mid + 1
            else:
                high = mid - 1

        # Calculate total significance
        total_significance = physics_prefix[i][0] + informatics_prefix[high][0]
        max_total_significance = max(max_total_significance, total_significance)

    return max_total_significance

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
d = int(data[2])

physics_cups = []
index = 3
for _ in range(n):
    c = int(data[index])
    w = int(data[index + 1])
    physics_cups.append((c, w))
    index += 2

informatics_cups = []
for _ in range(m):
    c = int(data[index])
    w = int(data[index + 1])
    informatics_cups.append((c, w))
    index += 2

# Get the result
result = max_significance(n, m, d, physics_cups, informatics_cups)
print(result)