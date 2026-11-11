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
    
    # Find a root for the tree (any node will work since it's a tree)
    root = 1
    
    # BFS to find the longest path from the root
    queue = deque([root])
    parent = {root: None}
    while queue:
        current = queue.popleft()
        for neighbor in adj_list[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    
    # Trace back to find the longest path
    longest_path = []
    current = max(parent, key=lambda x: len(parent[x]))
    while current is not None:
        longest_path.append(current)
        current = parent[current]
    
    # If the longest path has more than 2 nodes, it's impossible
    if len(longest_path) > 2:
        print("NO")
        return
    
    # Direct the edges
    result = []
    for u, v in edges:
        if u in parent and v == parent[u]:
            result.append('1')
        elif v in parent and u == parent[v]:
            result.append('0')
        else:
            # This case should not happen in a tree
            print("NO")
            return
    
    print("YES")
    print("".join(result))

if __name__ == "__main__":
    main()