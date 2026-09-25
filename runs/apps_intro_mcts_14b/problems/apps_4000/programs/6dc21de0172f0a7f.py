import sys
from collections import defaultdict, deque

def bfs(start, adj):
    dist = [-1] * len(adj)
    queue = deque([start])
    dist[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist

def find_longest_path(start, adj):
    dist = bfs(start, adj)
    farthest_node = max(range(len(adj)), key=lambda x: dist[x])
    return farthest_node, dist[farthest_node]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    adj = defaultdict(list)
    index = 1
    for _ in range(n - 1):
        a = int(data[index]) - 1
        b = int(data[index + 1]) - 1
        adj[a].append(b)
        adj[b].append(a)
        index += 2
    
    # Find the first longest path
    start_node, _ = find_longest_path(0, adj)
    _, first_longest_length = find_longest_path(start_node, adj)
    
    # Find the second longest path
    second_start_node, _ = find_longest_path(start_node, adj)
    _, second_longest_length = find_longest_path(second_start_node, adj)
    
    # Find the third longest path
    third_start_node, _ = find_longest_path(second_start_node, adj)
    _, third_longest_length = find_longest_path(third_start_node, adj)
    
    # The result is the sum of the lengths of the three longest paths
    res = first_longest_length + second_longest_length + third_longest_length
    
    # Output the result and the vertices
    print(res)
    print(start_node + 1, second_start_node + 1, third_start_node + 1)

if __name__ == "__main__":
    main()