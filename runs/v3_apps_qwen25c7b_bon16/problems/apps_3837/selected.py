def solve(n, m, s, a, b, c):
    # Create a list of tuples (student index, complexity, passes)
    students = [(i, b[i-1], c[i-1]) for i in range(1, n+1)]
    
    # Sort students by their ability level in descending order
    students.sort(key=lambda x: -x[1])
    
    # Sort bugs by their complexity in ascending order
    a.sort()
    
    # Initialize the result list and pass count
    result = [0] * m
    pass_count = 0
    
    # Assign bugs to students
    for i in range(m):
        assigned = False
        for j in range(n):
            if students[j][1] >= a[i]:
                # Check if assigning this bug would exceed the pass limit
                if pass_count + students[j][2] <= s:
                    result[i] = students[j][0]
                    pass_count += students[j][2]
                    assigned = True
                    break
        if not assigned:
            return "NO"
    
    return "YES\n" + " ".join(map(str, result))

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
m = int(data[1])
s = int(data[2])
a = list(map(int, data[3:3+m]))
b = list(map(int, data[3+m:3+m+n]))
c = list(map(int, data[3+m+n:]))

# Solve problem
result = solve(n, m, s, a, b, c)

# Print result
print(result)