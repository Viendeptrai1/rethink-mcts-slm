def is_rotationally_symmetrical(n, m, segments):
    # Create a list to store the next point for each point
    next_point = [-1] * (n + 1)
    
    # Fill the next_point array based on the given segments
    for a, b in segments:
        if next_point[a] == -1:
            next_point[a] = b
        else:
            return "No"
    
    # Check if the graph forms a single cycle
    visited = [False] * (n + 1)
    current = 1
    
    while True:
        if visited[current]:
            break
        visited[current] = True
        current = next_point[current]
    
    if not all(visited[1:]):
        return "No"
    
    # Find the length of the cycle
    cycle_length = 0
    current = 1
    while True:
        cycle_length += 1
        current = next_point[current]
        if current == 1:
            break
    
    # Check if the cycle length divides n
    if n % cycle_length != 0:
        return "No"
    
    return "Yes"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

segments = []
for i in range(m):
    a = int(data[2 + 2 * i]) - 1
    b = int(data[3 + 2 * i]) - 1
    segments.append((a, b))

# Output result
print(is_rotationally_symmetrical(n, m, segments))