import sys
import heapq

def max_projects(n, r, projects):
    # Sort projects by the required rating
    projects.sort()
    
    # Priority queue to store the current state of Polycarp's rating and the number of completed projects
    pq = []
    heapq.heappush(pq, (-r, 0))  # (negative rating, number of projects)
    
    # Dictionary to store the maximum number of projects that can be completed with a given rating
    max_projects_with_rating = {r: 0}
    
    while pq:
        current_rating, num_projects = heapq.heappop(pq)
        current_rating = -current_rating
        
        for a, b in projects:
            if current_rating >= a:
                new_rating = current_rating + b
                if new_rating >= 0:
                    new_num_projects = num_projects + 1
                    if new_rating not in max_projects_with_rating or new_num_projects > max_projects_with_rating[new_rating]:
                        max_projects_with_rating[new_rating] = new_num_projects
                        heapq.heappush(pq, (-new_rating, new_num_projects))
    
    return max(max_projects_with_rating.values())

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
r = int(data[1])
projects = []

index = 2
for i in range(n):
    a = int(data[index])
    b = int(data[index + 1])
    projects.append((a, b))
    index += 2

# Calculate and print the result
result = max_projects(n, r, projects)
print(result)