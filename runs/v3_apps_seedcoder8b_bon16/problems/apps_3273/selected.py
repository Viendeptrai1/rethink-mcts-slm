import sys
from collections import defaultdict

def find_overlap(a, b):
    for i in range(min(len(a), len(b)), 4, -1):
        if a[-i:] == b[:i]:
            return i
    return 0

def find_reconstruction(fragments):
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    for i, f1 in enumerate(fragments):
        for j, f2 in enumerate(fragments):
            if i != j:
                overlap = find_overlap(f1, f2)
                if overlap >= 5:
                    graph[i].append(j)
                    in_degree[j] += 1
    
    start = next(i for i in range(len(fragments)) if in_degree[i] == 0)
    visited = set()
    path = []
    
    def dfs(node):
        visited.add(node)
        path.append(node)
        for neighbor in graph[node]:
            if neighbor in visited:
                return False
            if not dfs(neighbor):
                return False
        return True
    
    if not dfs(start):
        return "AMBIGUOUS"
    
    if len(visited) != len(fragments):
        return "AMBIGUOUS"
    
    reconstruction = fragments[path[0]]
    for i in range(1, len(path)):
        overlap = find_overlap(fragments[path[i-1]], fragments[path[i]])
        reconstruction += fragments[path[i]][overlap:]
    
    return reconstruction

def main():
    n = int(input())
    fragments = [input().strip() for _ in range(n)]
    result = find_reconstruction(fragments)
    print(result)

if __name__ == "__main__":
    main()