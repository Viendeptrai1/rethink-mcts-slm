import sys
from collections import defaultdict

def expected_time_to_exit(N, M, paths):
    graph = defaultdict(list)
    for K, L in paths:
        graph[K].append(L)
        graph[L].append(K)
    
    def dfs(node, parent):
        nonlocal total_time, count
        if node == N - 1:
            return 1
        time = 0
        for neighbor in graph[node]:
            if neighbor != parent:
                time += dfs(neighbor, node)
        if time > 0:
            total_time += time + len(graph[node]) - 1
            count += 1
        return time + 1
    
    total_time = 0
    count = 0
    dfs(0, -1)
    return total_time / count

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    M = int(data[index + 1])
    index += 2
    
    paths = []
    for _ in range(M):
        K = int(data[index])
        L = int(data[index + 1])
        paths.append((K, L))
        index += 2
    
    result = expected_time_to_exit(N, M, paths)
    print(f"{result:.6f}")