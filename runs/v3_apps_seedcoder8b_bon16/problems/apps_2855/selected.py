import sys
from collections import defaultdict

def expected_time_to_exit(n, paths):
    graph = defaultdict(list)
    for k, l in paths:
        graph[k].append(l)
        graph[l].append(k)
    
    def dfs(node, visited):
        if node == n - 1:
            return 1
        if node in visited:
            return 0
        
        visited.add(node)
        total_time = 0
        for neighbor in graph[node]:
            total_time += dfs(neighbor, visited)
        visited.remove(node)
        
        return total_time + 1 / len(graph[node])
    
    return dfs(0, set()) - 1

def main():
    n, m = map(int, input().split())
    paths = [tuple(map(int, input().split())) for _ in range(m)]
    result = expected_time_to_exit(n, paths)
    print(f"{result:.6f}")

if __name__ == "__main__":
    main()