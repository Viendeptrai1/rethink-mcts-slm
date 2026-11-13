def min_essays(n, r, avg, grades):
    total_current = sum(a for a, _ in grades)
    needed_total = avg * n
    
    if total_current >= needed_total:
        return 0
    
    grades.sort(key=lambda x: (x[0], -x[1]))
    
    essays_needed = 0
    for a, b in grades:
        if a < r:
            improve = min(needed_total - total_current, r - a)
            essays_needed += improve * b
            total_current += improve
    
    return essays_needed

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
r = int(data[1])
avg = int(data[2])
grades = [(int(data[3 + 2*i]), int(data[4 + 2*i])) for i in range(n)]

# Output the result
print(min_essays(n, r, avg, grades))