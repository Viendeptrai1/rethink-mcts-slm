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
    
    # Create adjacency list
    adj_list = defaultdict(list)
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Check if the graph is a tree (connected and acyclic)
    if m != n - 1:
        print("NO")
        return
    
    # Perform BFS to check if we can orient edges without creating paths of length 2
    visited = [False] * (n + 1)
    queue = deque([1])
    visited[1] = True
    orientation = ['0'] * m
    
    while queue:
        current = queue.popleft()
        for neighbor in adj_list[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
                # Orient the edge from current to neighbor
                orientation[edges.index((current, neighbor))] = '0'
                orientation[edges.index((neighbor, current))] = '1'
    
    # If all nodes are visited, it's possible to orient the edges
    if all(visited[1:]):
        print("YES")
        print(''.join(orientation))
    else:
        print("NO")

if __name__ == "__main__":
    main()