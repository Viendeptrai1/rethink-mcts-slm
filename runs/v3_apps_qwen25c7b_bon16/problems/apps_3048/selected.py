import sys
from collections import defaultdict

def count_optimal_paths(N, edges):
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    
    total_paths = 0
    for node in range(1, N + 1):
        neighbors = list(graph[node])
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[i] not in graph[neighbors[j]]:
                    total_paths += 1
    
    return total_paths * 2

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    edges = [(int(data[2*i + 1]), int(data[2*i + 2])) for i in range(N - 1)]
    
    result = count_optimal_paths(N, edges)
    print(result)