from itertools import combinations

def max_students_to_lunch(n, groups, k, x, a, b):
    def can_take(lunches_needed):
        for r in range(1, n + 1):
            for combo in combinations(groups, r):
                if sum(combo) == lunches_needed:
                    return True
        return False

    min_students = a
    max_students = b
    max_possible = -1

    for students in range(min_students, max_students + 1):
        if students % x == 0 and can_take(students):
            max_possible = max(max_possible, students)

    return max_possible if max_possible != -1 else 'impossible'

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
groups = list(map(int, data[1:n+1]))
k, x, a, b = map(int, data[n+1:])

# Get result
result = max_students_to_lunch(n, groups, k, x, a, b)

# Print result
print(result)