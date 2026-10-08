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

def bfs(tree, start):
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    
    while queue:
        node = queue.popleft()
        for neighbor in tree[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    
    return parent

def find_min_companies(n, k, edges):
    tree = defaultdict(list)
    for u, v in edges:
        tree[u].append(v)
        tree[v].append(u)
    
    # Find a root of the tree
    root = 0
    parent = bfs(tree, root)
    
    # Function to count bad nodes for a given number of companies
    def count_bad_nodes(companies):
        bad_nodes = set()
        for node in range(n):
            if node == root:
                continue
            path = []
            current = node
            while current is not None:
                path.append(current)
                current = parent[current]
            
            color_count = defaultdict(int)
            for node in path:
                color_count[node] += 1
            
            for node in path:
                if color_count[node] > companies:
                    bad_nodes.add(node)
        
        return len(bad_nodes)
    
    # Binary search for the minimum number of companies
    left, right = 1, n - 1
    while left < right:
        mid = (left + right) // 2
        if count_bad_nodes(mid) <= k:
            right = mid
        else:
            left = mid + 1
    
    return left

def assign_companies(n, k, edges, min_companies):
    tree = defaultdict(list)
    for u, v in edges:
        tree[u].append(v)
        tree[v].append(u)
    
    root = 0
    parent = bfs(tree, root)
    
    companies = [0] * (n - 1)
    color = 1
    for i, (u, v) in enumerate(edges):
        if parent[u] == v:
            u, v = v, u
        
        if color > min_companies:
            color = 1
        
        companies[i] = color
        color += 1
    
    return companies

def main():
    n, k, edges = read_input()
    min_companies = find_min_companies(n, k, edges)
    companies = assign_companies(n, k, edges, min_companies)
    
    print(min_companies)
    print(" ".join(map(str, companies)))

if __name__ == "__main__":
    main()