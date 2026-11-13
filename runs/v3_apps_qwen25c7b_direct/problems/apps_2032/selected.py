import sys
from collections import defaultdict, deque

def max_defended_score(n, m, k, castles, portals):
    # Initialize graph and other data structures
    graph = defaultdict(list)
    for u, v in portals:
        graph[u].append(v)
    
    # Function to perform BFS and find the maximum importance of defended castles
    def bfs(start):
        queue = deque([start])
        visited = set([start])
        defended_importance = 0
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            if castles[current][0] <= k:
                k += castles[current][1]
                defended_importance += castles[current][2]
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return defended_importance
    
    # Check if it's possible to capture all castles
    total_warriors_needed = sum(castles[i][0] for i in range(n))
    if k + sum(castles[i][1] for i in range(n)) < total_warriors_needed:
        return -1
    
    # Try to capture each castle in sequence and calculate the maximum defended score
    max_score = 0
    for i in range(n):
        if castles[i][0] <= k:
            k += castles[i][1]
            max_score += castles[i][2]
            max_score = max(max_score, bfs(i))
        else:
            break
    
    return max_score

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

castles = []
index = 3
for _ in range(n):
    a = int(data[index])
    b = int(data[index + 1])
    c = int(data[index + 2])
    castles.append((a, b, c))
    index += 3

portals = []
for _ in range(m):
    u = int(data[index]) - 1
    v = int(data[index + 1]) - 1
    portals.append((u, v))
    index += 2

# Calculate and print the result
result = max_defended_score(n, m, k, castles, portals)
print(result)