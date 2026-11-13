def find_optimal_reconstruction(fragments):
    from collections import defaultdict, deque

    def overlap_length(a, b):
        max_overlap = 0
        min_len = min(len(a), len(b))
        for i in range(5, min_len):
            if a[-i:] == b[:i]:
                max_overlap = i
        return max_overlap

    n = len(fragments)
    graph = defaultdict(list)
    in_degree = [0] * n

    for i in range(n):
        for j in range(n):
            if i != j:
                olap = overlap_length(fragments[i], fragments[j])
                if olap >= 5:
                    graph[i].append((j, olap))
                    in_degree[j] += 1

    # Find all nodes with zero in-degree
    zero_in_degree = deque([i for i in range(n) if in_degree[i] == 0])

    if len(zero_in_degree) != 1:
        return "AMBIGUOUS"

    # Topological sort to find the path
    path = []
    while zero_in_degree:
        if len(zero_in_degree) > 1:
            return "AMBIGUOUS"
        node = zero_in_degree.popleft()
        path.append(node)
        for neighbor, _ in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)

    if len(path) != n:
        return "AMBIGUOUS"

    # Reconstruct the manuscript
    reconstructed = fragments[path[0]]
    for i in range(1, len(path)):
        prev_fragment = fragments[path[i - 1]]
        curr_fragment = fragments[path[i]]
        overlap = overlap_length(prev_fragment, curr_fragment)
        reconstructed += curr_fragment[overlap:]

    return reconstructed

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    fragments = data[1:n+1]
    
    result = find_optimal_reconstruction(fragments)
    print(result)

if __name__ == "__main__":
    main()