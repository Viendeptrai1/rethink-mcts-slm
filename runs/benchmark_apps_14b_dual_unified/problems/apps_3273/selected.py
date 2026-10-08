import sys

def reconstruct_manuscript(fragments):
    def overlap_length(a, b):
        max_len = min(len(a), len(b))
        for i in range(max_len, 4, -1):
            if a[-i:] == b[:i]:
                return i
        return 0

    def build_graph(fragments):
        graph = {}
        for i, a in enumerate(fragments):
            for j, b in enumerate(fragments):
                if i != j:
                    overlap = overlap_length(a, b)
                    if overlap >= 5:
                        if i not in graph:
                            graph[i] = []
                        graph[i].append((j, overlap))
        return graph

    def find_longest_path(graph, start, visited, path):
        visited.add(start)
        path.append(start)
        max_path = path[:]
        for neighbor, _ in graph.get(start, []):
            if neighbor not in visited:
                new_path = find_longest_path(graph, neighbor, visited, path)
                if len(new_path) > len(max_path):
                    max_path = new_path
        path.pop()
        visited.remove(start)
        return max_path

    n = len(fragments)
    graph = build_graph(fragments)
    longest_path = []
    for i in range(n):
        path = find_longest_path(graph, i, set(), [])
        if len(path) > len(longest_path):
            longest_path = path

    if len(longest_path) < n:
        return "AMBIGUOUS"

    reconstruction = fragments[longest_path[0]]
    for i in range(1, len(longest_path)):
        idx = longest_path[i]
        overlap = overlap_length(fragments[longest_path[i-1]], fragments[idx])
        reconstruction += fragments[idx][overlap:]

    return reconstruction

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    n = int(data[0])
    fragments = data[1:]
    result = reconstruct_manuscript(fragments)
    print(result)