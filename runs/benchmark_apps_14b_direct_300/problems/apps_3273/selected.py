import sys

def find_optimal_reconstruction(fragments):
    n = len(fragments)
    graph = {i: [] for i in range(n)}
    
    for i in range(n):
        for j in range(n):
            if i != j:
                overlap_length = 0
                for k in range(5, min(len(fragments[i]), len(fragments[j])) + 1):
                    if fragments[i][-k:] == fragments[j][:k]:
                        overlap_length = k
                if overlap_length > 0:
                    graph[i].append((j, overlap_length))
    
    def dfs(node, visited, path):
        visited.add(node)
        path.append(node)
        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, visited, path)
    
    paths = []
    for start in range(n):
        visited = set()
        path = []
        dfs(start, visited, path)
        if len(path) == n:
            paths.append(path)
    
    if len(paths) != 1:
        return "AMBIGUOUS"
    
    path = paths[0]
    reconstruction = fragments[path[0]]
    for i in range(1, n):
        overlap_length = 0
        for k in range(5, min(len(fragments[path[i-1]]), len(fragments[path[i]])) + 1):
            if fragments[path[i-1]][-k:] == fragments[path[i]][:k]:
                overlap_length = k
        reconstruction += fragments[path[i]][overlap_length:]
    
    return reconstruction

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    n = int(data[0])
    fragments = data[1:]
    result = find_optimal_reconstruction(fragments)
    print(result)