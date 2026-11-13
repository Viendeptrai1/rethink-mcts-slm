def solve():
    import sys
    from collections import defaultdict, deque

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
    
    # Create adjacency list
    adj = defaultdict(list)
    for x, y in edges:
        adj[x].append(y)
        adj[y].append(x)
    
    # BFS to find the farthest node from an arbitrary node
    def bfs(start):
        visited = [-1] * n
        queue = deque([(start, 0)])
        visited[start] = 0
        farthest_node = start
        max_distance = 0
        
        while queue:
            node, dist = queue.popleft()
            for neighbor in adj[node]:
                if visited[neighbor] == -1:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))
                    if visited[neighbor] > max_distance:
                        max_distance = visited[neighbor]
                        farthest_node = neighbor
        
        return farthest_node, max_distance
    
    # Find the diameter of the tree
    u, _ = bfs(0)
    v, diameter = bfs(u)
    
    # The number of companies needed is at most (diameter + 1) // 2
    r = (diameter + 1) // 2
    
    # If r > k, it's impossible to satisfy the condition
    if r > k:
        print("UNSOLVABLE##")
        return
    
    # Assign companies to roads
    result = [0] * (n - 1)
    current_company = 1
    
    # Function to assign companies along the path from u to v
    def assign_companies(u, v, parent, road_index):
        nonlocal current_company
        if u == v:
            return
        
        # Assign the current company to the road
        result[road_index] = current_company
        
        # Find the next node in the path
        next_node = -1
        for neighbor in adj[u]:
            if neighbor != parent:
                next_node = neighbor
                break
        
        # Alternate companies every time we move to a new road
        current_company = current_company % r + 1
        
        # Recurse to the next node
        assign_companies(next_node, v, u, road_index + 1)
    
    # Find the path from u to v
    path = []
    current = v
    while current != u:
        path.append(current)
        for neighbor in adj[current]:
            if visited[neighbor] == visited[current] - 1:
                current = neighbor
                break
    path.append(u)
    
    # Assign companies along the path
    for i in range(len(path) - 1):
        assign_companies(path[i], path[i + 1], -1, i)
    
    # Print the result
    print(r)
    print(" ".join(map(str, result)))