import sys
from collections import defaultdict, deque

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    edges = []
    for _ in range(m):
        u = int(data[index]) - 1
        v = int(data[index + 1]) - 1
        edges.append((u, v))
        index += 2
    
    # Create adjacency list
    adj_list = defaultdict(list)
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Initialize in-degree count
    in_degree = [0] * n
    
    # Greedy algorithm to orient edges
    orientation = []
    for u, v in edges:
        if in_degree[u] < in_degree[v]:
            orientation.append('0')
            in_degree[v] += 1
        else:
            orientation.append('1')
            in_degree[u] += 1
    
    # Check if the resulting graph has any path of length two or greater
    def has_path_of_length_two_or_greater():
        visited = [False] * n
        queue = deque()
        
        for i in range(n):
            if in_degree[i] == 0:
                queue.append(i)
                visited[i] = True
        
        while queue:
            node = queue.popleft()
            for neighbor in adj_list[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return sum(visited) != n
    
    if has_path_of_length_two_or_greater():
        print("NO")
    else:
        print("YES")
        print(''.join(orientation))

if __name__ == "__main__":
    main()