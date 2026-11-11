import sys
import heapq

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    edges = []
    index = 2
    for _ in range(n - 1):
        x = int(data[index]) - 1
        y = int(data[index + 1]) - 1
        edges.append((x, y))
        index += 2
    
    return n, k, edges

def bfs(graph, start, parent):
    queue = [start]
    visited = set([start])
    while queue:
        node = queue.pop(0)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    return visited

def find_min_companies(n, k, edges):
    from collections import defaultdict, deque
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    def is_valid(r):
        parent = [-1] * n
        bad_cities = set()
        
        for i in range(n):
            if parent[i] == -1:
                visited = bfs(graph, i, parent)
                degree = [0] * n
                for node in visited:
                    for neighbor in graph[node]:
                        if neighbor in visited:
                            degree[node] += 1
                
                pq = []
                for node in visited:
                    if degree[node] > 1:
                        heapq.heappush(pq, (-degree[node], node))
                
                used = [False] * r
                while pq:
                    d, node = heapq.heappop(pq)
                    assigned = False
                    for j in range(r):
                        if not used[j]:
                            used[j] = True
                            assigned = True
                            break
                    if not assigned:
                        return False
                    for neighbor in graph[node]:
                        if neighbor in visited:
                            degree[neighbor] -= 1
                            if degree[neighbor] > 1:
                                heapq.heappush(pq, (-degree[neighbor], neighbor))
        
        return len(bad_cities) <= k
    
    low, high = 1, n - 1
    while low < high:
        mid = (low + high) // 2
        if is_valid(mid):
            high = mid
        else:
            low = mid + 1
    
    return low

def assign_roads(n, k, edges, r):
    from collections import defaultdict, deque
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    parent = [-1] * n
    bad_cities = set()
    
    for i in range(n):
        if parent[i] == -1:
            visited = bfs(graph, i, parent)
            degree = [0] * n
            for node in visited:
                for neighbor in graph[node]:
                    if neighbor in visited:
                        degree[node] += 1
            
            pq = []
            for node in visited:
                if degree[node] > 1:
                    heapq.heappush(pq, (-degree[node], node))
            
            used = [False] * r
            assignments = {}
            while pq:
                d, node = heapq.heappop(pq)
                assigned = False
                for j in range(r):
                    if not used[j]:
                        used[j] = True
                        assigned = True
                        assignments[node] = j
                        break
                if not assigned:
                    return None
                for neighbor in graph[node]:
                    if neighbor in visited:
                        degree[neighbor] -= 1
                        if degree[neighbor] > 1:
                            heapq.heappush(pq, (-degree[neighbor], neighbor))
    
    result = []
    for u, v in edges:
        if u in assignments:
            result.append(assignments[u] + 1)
        else:
            result.append(assignments[v] + 1)
    
    return result

def main():
    n, k, edges = read_input()
    r = find_min_companies(n, k, edges)
    assignments = assign_roads(n, k, edges, r)
    print(r)
    print(" ".join(map(str, assignments)))

if __name__ == "__main__":
    main()