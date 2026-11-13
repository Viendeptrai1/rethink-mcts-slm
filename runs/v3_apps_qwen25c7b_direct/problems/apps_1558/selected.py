def min_essays_to_scholarship(n, r, avg, grades):
    total_current_grade = sum(a for a, _ in grades)
    target_total_grade = avg * n
    
    if total_current_grade >= target_total_grade:
        return 0
    
    essays_needed = 0
    grades.sort(key=lambda x: x[1])
    
    while total_current_grade < target_total_grade:
        _, b_i = grades.pop()
        if total_current_grade + (r - 1) * b_i >= target_total_grade:
            essays_needed += (target_total_grade - total_current_grade) // b_i
            break
        else:
            total_current_grade += (r - 1) * b_i
            essays_needed += (r - 1)
    
    return essays_needed

# Example usage:
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

print(min_essays_to_scholarship(n, r, avg, grades))