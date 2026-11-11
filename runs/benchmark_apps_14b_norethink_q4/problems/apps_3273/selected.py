import sys

def find_longest_path(graph, start, visited, path):
    visited[start] = True
    path.append(start)
    
    max_path = path[:]
    for neighbor in graph[start]:
        if not visited[neighbor]:
            new_path = find_longest_path(graph, neighbor, visited, path)
            if len(new_path) > len(max_path):
                max_path = new_path
    
    path.pop()
    visited[start] = False
    return max_path

def build_graph(fragments):
    graph = {i: [] for i in range(len(fragments))}
    for i in range(len(fragments)):
        for j in range(len(fragments)):
            if i != j:
                overlap_length = min(len(fragments[i]), len(fragments[j]))
                for k in range(5, overlap_length + 1):
                    if fragments[i][-k:] == fragments[j][:k]:
                        graph[i].append(j)
                        break
    return graph

def reconstruct_manuscript(fragments):
    n = len(fragments)
    graph = build_graph(fragments)
    
    max_path = []
    for i in range(n):
        visited = [False] * n
        path = find_longest_path(graph, i, visited, [])
        if len(path) > len(max_path):
            max_path = path
    
    if len(max_path) < n:
        return "AMBIGUOUS"
    
    reconstruction = fragments[max_path[0]]
    for i in range(1, len(max_path)):
        overlap_length = min(len(fragments[max_path[i-1]]), len(fragments[max_path[i]]))
        for k in range(5, overlap_length + 1):
            if fragments[max_path[i-1]][-k:] == fragments[max_path[i]][:k]:
                reconstruction += fragments[max_path[i]][k:]
                break
    
    return reconstruction

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    fragments = data[1:]
    
    result = reconstruct_manuscript(fragments)
    print(result)

if __name__ == "__main__":
    main()