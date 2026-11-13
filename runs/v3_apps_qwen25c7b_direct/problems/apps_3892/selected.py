from collections import defaultdict, deque

def min_delivery_time(n, m, candies):
    graph = defaultdict(list)
    for a, b in candies:
        graph[a].append(b)
    
    def bfs(start):
        visited = [False] * (n + 1)
        queue = deque([(start, 0)])
        visited[start] = True
        total_time = 0
        
        while queue:
            current, time = queue.popleft()
            total_time += time
            
            for neighbor in graph[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, 1))
        
        return total_time
    
    result = []
    for i in range(1, n + 1):
        result.append(bfs(i))
    
    return result

# Example usage:
# n, m = map(int, input().split())
# candies = [tuple(map(int, input().split())) for _ in range(m)]
# print(" ".join(map(str, min_delivery_time(n, m, candies))))