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
    for _ in range(n - 1):
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
        queue = deque([start])
        visited = [False] * n
        visited[start] = True
        parent = [-1] * n
        level = 0
        
        while queue:
            size = len(queue)
            for _ in range(size):
                node = queue.popleft()
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        parent[neighbor] = node
                        queue.append(neighbor)
            level += 1
        
        farthest_node = node
        return farthest_node, parent, level
    
    # First BFS to find one end of the diameter
    _, parent, _ = bfs(root)
    
    # Second BFS to find the other end of the diameter
    farthest_node, parent, diameter = bfs(parent[root])
    
    # The center(s) of the tree
    center = farthest_node
    if diameter % 2 == 0:
        center = parent[farthest_node]
    
    # BFS to assign companies
    queue = deque([center])
    visited = [False] * n
    visited[center] = True
    company_assignment = [0] * (n - 1)
    current_company = 1
    
    while queue:
        size = len(queue)
        for _ in range(size):
            node = queue.popleft()
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    company_assignment[edges.index((min(node, neighbor), max(node, neighbor)))] = current_company
                    queue.append(neighbor)
        current_company += 1
    
    # Check the number of bad cities
    bad_cities = 0
    company_count = defaultdict(int)
    for u, v in edges:
        company_count[company_assignment[edges.index((min(u, v), max(u, v)))]] += 1
        if company_count[company_assignment[edges.index((min(u, v), max(u, v)))]] > 1:
            bad_cities += 1
    
    # If the number of bad cities exceeds k, we need more companies
    while bad_cities > k:
        current_company += 1
        for i in range(n - 1):
            if company_assignment[i] == current_company:
                company_assignment[i] = current_company + 1
                bad_cities -= 1
                if bad_cities <= k:
                    break
    
    return current_company, company_assignment

def main():
    n, k, edges = read_input()
    r, company_assignment = find_min_companies(n, k, edges)
    print(r)
    print(' '.join(map(str, company_assignment)))

if __name__ == "__main__":
    main()