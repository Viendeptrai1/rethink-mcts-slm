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
        visited[node] = True
        path.append(node)
        
        if all(visited[neighbor] for neighbor, _ in graph[node]):
            return path
        
        for neighbor, _ in graph[node]:
            if not visited[neighbor]:
                result = dfs(neighbor, visited, path[:])
                if result:
                    return result
        
        return None
    
    max_path = []
    for start in range(n):
        visited = [False] * n
        path = dfs(start, visited, [])
        if path and len(path) > len(max_path):
            max_path = path
    
    if len(max_path) < n:
        return "AMBIGUOUS"
    
    reconstruction = fragments[max_path[0]]
    for i in range(1, len(max_path)):
        _, overlap_length = next((neighbor, overlap_length) for neighbor, overlap_length in graph[max_path[i-1]] if neighbor == max_path[i])
        reconstruction += fragments[max_path[i]][overlap_length:]
    
    return reconstruction

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    n = int(data[0])
    fragments = data[1:]
    result = find_optimal_reconstruction(fragments)
    print(result)