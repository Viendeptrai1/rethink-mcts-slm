def solve():
    import sys
    from collections import defaultdict, deque
    
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    roads = []
    index = 2
    for _ in range(n - 1):
        x = int(data[index]) - 1
        y = int(data[index + 1]) - 1
        roads.append((x, y))
        index += 2
    
    # Create adjacency list for the tree
    adj = defaultdict(list)
    for x, y in roads:
        adj[x].append(y)
        adj[y].append(x)
    
    # BFS to determine the degree of each node
    degree = [0] * n
    for i in range(n):
        degree[i] = len(adj[i])
    
    # We need to determine the minimal number of companies r
    # such that the number of cities with two or more roads from one company is <= k
    
    # Start with a simple BFS coloring strategy
    company = [0] * (n - 1)
    used_companies = 0
    
    # We will use a queue to perform BFS
    queue = deque()
    
    # Start BFS from any node, here we start from node 0
    queue.append(0)
    visited = [False] * n
    visited[0] = True
    
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
                
                # Assign the next available company to this road
                used_companies += 1
                company[len(company) - degree[node]] = used_companies
    
    # Output the result
    print(used_companies)
    print(' '.join(map(str, company)))