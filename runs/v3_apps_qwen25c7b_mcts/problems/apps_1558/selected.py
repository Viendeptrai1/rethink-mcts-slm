def min_essays(n, r, avg, grades):
    current_total = sum(grade[0] for grade in grades)
    target_total = avg * n
    additional_needed = max(target_total - current_total, 0)

    total_essays = 0
    for grade, cost in sorted(grades, key=lambda x: x[1]):
        if additional_needed <= 0:
            break
        increment = min(additional_needed, r - grade)
        total_essays += increment * cost
        additional_needed -= increment

    return total_essays

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
r = int(data[1])
avg = int(data[2])

grades = []
for i in range(n):
    a_i = int(data[3 + 2 * i])
    b_i = int(data[4 + 2 * i])
    grades.append((a_i, b_i))

# Output the result
print(min_essays(n, r, avg, grades))