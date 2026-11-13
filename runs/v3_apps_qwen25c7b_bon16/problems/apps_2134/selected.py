from typing import List

def max_calm_group_sum(n: int, a: List[int], b: List[int]) -> int:
    max_sum = 0
    for i in range(1 << n):
        if i & (i - 1) == 0:  # Skip single student groups
            continue
        students = []
        for j in range(n):
            if i & (1 << j):
                students.append((a[j], b[j]))
        calm = True
        for k in range(len(students)):
            for l in range(k + 1, len(students)):
                if (students[k][0] & ~students[l][0]) != 0 or (students[l][0] & ~students[k][0]) != 0:
                    calm = False
                    break
            if not calm:
                break
        if calm:
            current_sum = sum(student[1] for student in students)
            max_sum = max(max_sum, current_sum)
    return max_sum

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:n+1]))
b = list(map(int, data[n+1:]))

# Calculate and print the result
print(max_calm_group_sum(n, a, b))