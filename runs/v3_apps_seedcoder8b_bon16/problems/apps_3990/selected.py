import sys
from collections import deque

def solve(n, m, railways):
    graph = [[] for _ in range(n+1)]
    roads = [[1] * (n+1) for _ in range(n+1)]
    
    for u, v in railways:
        graph[u].append(v)
        graph[v].append(u)
        roads[u][v] = roads[v][u] = 0
    
    def bfs(start, is_train):
        queue = deque([(start, 0)])
        visited = [False] * (n+1)
        visited[start] = True
        
        while queue:
            node, time = queue.popleft()
            
            if node == n:
                return time
            
            for neighbor in range(1, n+1):
                if not visited[neighbor] and ((is_train and roads[node][neighbor]) or (not is_train and not roads[node][neighbor])):
                    visited[neighbor] = True
                    queue.append((neighbor, time + 1))
        
        return float('inf')
    
    train_time = bfs(1, True)
    bus_time = bfs(1, False)
    
    if train_time == float('inf') or bus_time == float('inf'):
        return -1
    
    return max(train_time, bus_time)

def main():
    n, m = map(int, input().split())
    railways = [tuple(map(int, input().split())) for _ in range(m)]
    
    result = solve(n, m, railways)
    print(result)

if __name__ == "__main__":
    main()