import sys
import heapq

def max_defended_castles_score(n, m, k, castles, portals):
    # Initialize the graph
    graph = [[] for _ in range(n)]
    for u, v in portals:
        graph[u-1].append(v-1)
    
    # Priority queue to store the state (current castle, current score, current army size)
    pq = [(-castles[0][2], 0, k)]
    visited = set()
    
    while pq:
        score, i, army_size = heapq.heappop(pq)
        score = -score
        
        if (i, army_size) in visited:
            continue
        visited.add((i, army_size))
        
        if i == n:
            return score
        
        # Hire warriors from the current castle
        army_size += castles[i][1]
        
        # Capture the next castle if possible
        if i + 1 < n and army_size >= castles[i+1][0]:
            new_score = score + castles[i+1][2]
            new_army_size = army_size - castles[i+1][0]
            heapq.heappush(pq, (-new_score, i+1, new_army_size))
        
        # Defend the current castle
        if army_size > 0:
            new_score = score + castles[i][2]
            new_army_size = army_size - 1
            heapq.heappush(pq, (-new_score, i, new_army_size))
        
        # Use portals to defend other castles
        for j in graph[i]:
            if army_size > 0:
                new_score = score + castles[j][2]
                new_army_size = army_size - 1
                heapq.heappush(pq, (-new_score, i, new_army_size))
    
    return -1

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
    u = int(data[index])
    v = int(data[index + 1])
    portals.append((u, v))
    index += 2

# Output the result
print(max_defended_castles_score(n, m, k, castles, portals))