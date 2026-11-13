def solve(n, m, s, a, b, c):
    # Sort students based on their ability levels in descending order
    students = sorted(range(n), key=lambda x: -b[x])
    
    # Initialize the result list with zeros
    result = [0] * m
    
    # Initialize the total passes used
    total_passes = 0
    
    # Iterate over each bug
    for i in range(m):
        # Find a student who can fix the current bug
        for student in students:
            if b[student] >= a[i]:
                # Check if adding this student's passes would exceed the limit
                if total_passes + c[student] <= s:
                    # Assign the student to fix the bug
                    result[i] = student + 1
                    # Update the total passes used
                    total_passes += c[student]
                    break
        
        # If no suitable student was found, return 'NO'
        if result[i] == 0:
            return "NO"
    
    # Return 'YES' and the result list
    return "YES\n" + " ".join(map(str, result))

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
m = int(data[1])
s = int(data[2])
a = list(map(int, data[3:3+m]))
b = list(map(int, data[3+m:3+2*m]))
c = list(map(int, data[3+2*m:]))

# Solve the problem
result = solve(n, m, s, a, b, c)

# Print the result
print(result)