import sys
from collections import defaultdict, deque

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    edges = []
    for i in range(m):
        u = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        edges.append((u, v))
    
    # Check if the graph is a tree
    if m != n - 1:
        print("NO")
        return
    
    # Build the adjacency list
    adj_list = defaultdict(list)
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Find a leaf node
    leaf = None
    for node in adj_list:
        if len(adj_list[node]) == 1:
            leaf = node
            break
    
    # Perform BFS to find the longest path
    queue = deque([leaf])
    parent = {leaf: None}
    while queue:
        current = queue.popleft()
        for neighbor in adj_list[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    
    # Trace back the longest path
    path = []
    current = max(parent, key=lambda x: len(parent[x]))
    while current is not None:
        path.append(current)
        current = parent[current]
    
    # Direct the edges
    result = []
    for u, v in edges:
        if u in path and v in path:
            if path.index(u) < path.index(v):
                result.append('0')
            else:
                result.append('1')
        elif u in path:
            result.append('0')
        elif v in path:
            result.append('1')
        else:
            result.append('0')
    
    print("YES")
    print("".join(result))

if __name__ == "__main__":
    main()