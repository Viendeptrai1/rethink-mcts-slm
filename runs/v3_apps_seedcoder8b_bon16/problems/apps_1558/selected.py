def min_essays_for_scholarship(n, r, avg, exams):
    total_points = sum(a for a, _ in exams)
    total_essays = 0
    required_total_points = avg * n

    if total_points >= required_total_points:
        return 0

    exams.sort(key=lambda x: (x[1], -x[0]))

    for a_i, b_i in exams:
        if total_points >= required_total_points:
            break

        needed_points = required_total_points - total_points
        if a_i < r:
            increase = min(needed_points, r - a_i)
            total_points += increase
            total_essays += increase * b_i

    return total_essays

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
r = int(data[1])
avg = int(data[2])
exams = []
index = 3
for _ in range(n):
    a_i = int(data[index])
    b_i = int(data[index + 1])
    exams.append((a_i, b_i))
    index += 2

# Get the result
result = min_essays_for_scholarship(n, r, avg, exams)

# Print the result
print(result)