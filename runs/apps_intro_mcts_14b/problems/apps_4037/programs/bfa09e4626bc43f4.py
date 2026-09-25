import sys

def max_projects(n, r, projects):
    # Sort projects based on the difference (a_i - b_i)
    projects.sort(key=lambda x: x[0] - x[1])
    
    # Initialize variables
    max_size = 0
    current_rating = r
    
    # Iterate over all possible subsets of projects
    for i in range(1 << n):
        valid = True
        current_rating = r
        count = 0
        
        for j in range(n):
            if i & (1 << j):
                a_i, b_i = projects[j]
                if current_rating < a_i:
                    valid = False
                    break
                current_rating += b_i
                if current_rating < 0:
                    valid = False
                    break
                count += 1
        
        if valid:
            max_size = max(max_size, count)
    
    return max_size

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
r = int(data[1])
projects = []

index = 2
for _ in range(n):
    a_i = int(data[index])
    b_i = int(data[index + 1])
    projects.append((a_i, b_i))
    index += 2

# Calculate and print the result
result = max_projects(n, r, projects)
print(result)