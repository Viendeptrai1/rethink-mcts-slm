def max_significance(n, m, d, physics_cups, informatics_cups):
    physics_cups.sort(key=lambda x: (-x[0], x[1]))
    informatics_cups.sort(key=lambda x: (-x[0], x[1]))

    def binary_search(cups, target_width):
        left, right = 0, len(cups)
        while left < right:
            mid = (left + right) // 2
            if sum(cups[i][1] for i in range(mid + 1)) <= target_width:
                left = mid + 1
            else:
                right = mid
        return left

    max_sig = 0
    for i in range(min(n, m)):
        remaining_width = d - physics_cups[i][1]
        if remaining_width > 0:
            num_informatics = binary_search(informatics_cups, remaining_width)
            if num_informatics > 0:
                max_sig = max(max_sig, physics_cups[i][0] + sum(informatics_cups[j][0] for j in range(num_informatics)))

    return max_sig

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
d = int(data[2])

physics_cups = []
for i in range(n):
    c_i = int(data[3 + 2 * i])
    w_i = int(data[4 + 2 * i])
    physics_cups.append((c_i, w_i))

informatics_cups = []
for i in range(m):
    c_j = int(data[3 + 2 * n + 2 * i])
    w_j = int(data[4 + 2 * n + 2 * i])
    informatics_cups.append((c_j, w_j))

print(max_significance(n, m, d, physics_cups, informatics_cups))