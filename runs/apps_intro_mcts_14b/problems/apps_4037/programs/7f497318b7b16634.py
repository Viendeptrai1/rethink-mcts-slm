import sys

def max_projects(n, r, projects):
    # Sort projects by the required rating in ascending order
    projects.sort(key=lambda x: x[0])
    
    # Initialize the count of completed projects
    count = 0
    
    # Iterate over the sorted projects
    for a, b in projects:
        # Check if Polycarp can complete the current project
        if r >= a:
            # Update Polycarp's rating after completing the project
            r += b
            # Ensure Polycarp's rating does not fall below zero
            if r < 0:
                r = 0
            # Increment the count of completed projects
            count += 1
    
    return count

# Read input from standard input
input = sys.stdin.read
data = input().split()

# Parse the input values
n = int(data[0])
r = int(data[1])
projects = []
index = 2
for i in range(n):
    a = int(data[index])
    b = int(data[index + 1])
    projects.append((a, b))
    index += 2

# Calculate the maximum possible size of the subset of projects
result = max_projects(n, r, projects)

# Print the result to standard output
print(result)