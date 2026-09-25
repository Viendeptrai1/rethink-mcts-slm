import sys
from collections import deque

def max_projects(n, r, projects):
    # Sort projects by the required rating in ascending order
    projects.sort(key=lambda x: x[0])
    
    # Initialize a deque to keep track of the maximum rating we can reach
    max_rating = deque([r])
    
    # Iterate over each project
    for a, b in projects:
        # Remove ratings from the front of the deque that are less than the required rating for the current project
        while max_rating and max_rating[0] < a:
            max_rating.popleft()
        
        # If there are no ratings left in the deque, it means we cannot complete the current project
        if not max_rating:
            continue
        
        # Get the maximum rating we can reach before starting the current project
        current_max_rating = max_rating[0]
        
        # Calculate the new rating after completing the current project
        new_rating = current_max_rating + b
        
        # If the new rating is non-negative, add it to the deque
        if new_rating >= 0:
            # Maintain the deque in decreasing order
            while max_rating and max_rating[-1] <= new_rating:
                max_rating.pop()
            max_rating.append(new_rating)
    
    # The size of the deque represents the maximum number of projects we can complete
    return len(max_rating)

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
r = int(data[1])
projects = []

index = 2
for _ in range(n):
    a = int(data[index])
    b = int(data[index + 1])
    projects.append((a, b))
    index += 2

# Calculate and print the result
result = max_projects(n, r, projects)
print(result)