import sys
from collections import defaultdict

def count_valid_paintings(N, edges, M, restrictions):
    def dfs(node, parent, black_edges):
        if node == target:
            return 1
        count = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                if (node, neighbor) in black_edges or (neighbor, node) in black_edges:
                    count += dfs(neighbor, node, black_edges)
                else:
                    black_edges.add((node, neighbor))
                    count += dfs(neighbor, node, black_edges)
                    black_edges.remove((node, neighbor))
        return count

    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    total_ways = 0
    for u, v in restrictions:
        target = v
        total_ways += dfs(u, -1, set())

    return total_ways

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    edges = []
    for _ in range(N - 1):
        a = int(data[index])
        b = int(data[index + 1])
        edges.append((a, b))
        index += 2
    
    M = int(data[index])
    index += 1
    restrictions = []
    for _ in range(M):
        u = int(data[index])
        v = int(data[index + 1])
        restrictions.append((u, v))
        index += 2
    
    result = count_valid_paintings(N, edges, M, restrictions)
    print(result)

if __name__ == "__main__":
    main()