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
    _, first_end = bfs(root)
    
    # Second BFS to find the other end of the diameter
    second_end, diameter = bfs(first_end)
    
    # The diameter of the tree
    diameter_edges = set()
    visited = [False] * n
    queue = deque([(first_end, 0)])
    visited[first_end] = True
    
    while queue:
        node, distance = queue.popleft()
        if distance == diameter // 2:
            diameter_edges.add(node)
        elif distance > diameter // 2:
            break
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, distance + 1))
    
    # Assign companies to edges
    companies = [0] * (n - 1)
    company_count = 1
    
    for i, (u, v) in enumerate(edges):
        if u in diameter_edges or v in diameter_edges:
            companies[i] = company_count
            company_count += 1
        else:
            companies[i] = company_count
    
    # Check if the number of bad cities exceeds k
    bad_cities = 0
    city_count = defaultdict(int)
    
    for i, (u, v) in enumerate(edges):
        city_count[u] += 1
        city_count[v] += 1
    
    for count in city_count.values():
        if count > company_count:
            bad_cities += 1
    
    while bad_cities > k:
        company_count += 1
        bad_cities = 0
        for count in city_count.values():
            if count > company_count:
                bad_cities += 1
    
    return company_count, companies

def main():
    n, k, edges = read_input()
    company_count, companies = find_min_companies(n, k, edges)
    print(company_count)
    print(' '.join(map(str, companies)))

if __name__ == "__main__":
    main()