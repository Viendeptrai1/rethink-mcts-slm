import sys
from collections import defaultdict, deque

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    edges = []
    index = 2
    for _ in range(n-1):
        x = int(data[index]) - 1
        y = int(data[index + 1]) - 1
        edges.append((x, y))
        index += 2
    
    return n, k, edges

def find_min_companies(n, k, edges):
    # Build the graph
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Find the root of the tree (any node can be the root)
    root = 0
    
    # BFS to find the diameter of the tree
    def bfs(start):
        queue = deque([(start, 0)])
        visited = [False] * n
        visited[start] = True
        farthest_node = start
        max_distance = 0
        
        while queue:
            node, distance = queue.popleft()
            if distance > max_distance:
                max_distance = distance
                farthest_node = node
            
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, distance + 1))
        
        return farthest_node, max_distance
    
    # First BFS to find one end of the diameter
    _, distance = bfs(root)
    # Second BFS to find the other end of the diameter
    farthest_node, _ = bfs(distance)
    
    # The diameter of the tree
    diameter = distance
    
    # If the diameter is less than or equal to k+1, we can use 1 company
    if diameter <= k + 1:
        return 1, [1] * (n - 1)
    
    # Otherwise, we need to use more companies
    # We will use a greedy approach to assign companies
    companies = [0] * (n - 1)
    company_count = 0
    
    # BFS to assign companies
    queue = deque([farthest_node])
    visited = [False] * n
    visited[farthest_node] = True
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                company_count += 1
                companies[edges.index((node, neighbor))] = company_count
                companies[edges.index((neighbor, node))] = company_count
                queue.append(neighbor)
    
    # If the number of companies used is greater than k+1, we need to reduce it
    if company_count > k + 1:
        # We will use a binary search to find the minimum number of companies
        left = 2
        right = company_count
        while left < right:
            mid = (left + right) // 2
            if can_assign_with_k_conflicts(n, k, edges, mid):
                right = mid
            else:
                left = mid + 1
        
        company_count = left
    
    # Assign companies again with the minimum number of companies
    companies = [0] * (n - 1)
    company_count = 0
    visited = [False] * n
    visited[farthest_node] = True
    queue = deque([farthest_node])
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                company_count += 1
                companies[edges.index((node, neighbor))] = company_count % company_count + 1
                companies[edges.index((neighbor, node))] = company_count % company_count + 1
                queue.append(neighbor)
    
    return company_count, companies

def can_assign_with_k_conflicts(n, k, edges, r):
    # Build the graph
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # BFS to find the diameter of the tree
    def bfs(start):
        queue = deque([(start, 0)])
        visited = [False] * n
        visited[start] = True
        farthest_node = start
        max_distance = 0
        
        while queue:
            node, distance = queue.popleft()
            if distance > max_distance:
                max_distance = distance
                farthest_node = node
            
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, distance + 1))
        
        return farthest_node, max_distance
    
    # First BFS to find one end of the diameter
    _, distance = bfs(0)
    # Second BFS to find the other end of the diameter
    farthest_node, _ = bfs(distance)
    
    # The diameter of the tree
    diameter = distance
    
    # If the diameter is less than or equal to k+1, we can use 1 company
    if diameter <= k + 1:
        return True
    
    # Otherwise, we need to use more companies
    # We will use a greedy approach to assign companies
    companies = [0] * (n - 1)
    company_count = 0
    
    # BFS to assign companies
    queue = deque([farthest_node])
    visited = [False] * n
    visited[farthest_node] = True
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                company_count += 1
                companies[edges.index((node, neighbor))] = company_count % r + 1
                companies[edges.index((neighbor, node))] = company_count % r + 1
                queue.append(neighbor)
    
    # Check the number of conflicts
    conflicts = 0
    for i in range(n):
        count = defaultdict(int)
        for neighbor in graph[i]:
            count[companies[edges.index((i, neighbor))]] += 1
        for c in count.values():
            if c > 1:
                conflicts += 1
    
    return conflicts <= k

def main():
    n, k, edges = read_input()
    r, companies = find_min_companies(n, k, edges)
    print(r)
    print(" ".join(map(str, companies)))

if __name__ == "__main__":
    main()