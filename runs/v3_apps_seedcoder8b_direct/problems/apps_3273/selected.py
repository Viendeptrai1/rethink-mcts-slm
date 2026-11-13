def find_optimal_reconstruction(fragments):
    from collections import defaultdict

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
                overlap = overlap_length(fragments[i], fragments[j])
                if overlap >= 5:
                    graph[i].append((j, overlap))
                    in_degree[j] += 1

    # Find the starting point (node with in-degree 0)
    start = -1
    for i in range(n):
        if in_degree[i] == 0:
            if start == -1:
                start = i
            else:
                return "AMBIGUOUS"

    if start == -1:
        return "AMBIGUOUS"

    # Topological sort
    order = []
    queue = [start]
    while queue:
        node = queue.pop(0)
        order.append(node)
        for neighbor, _ in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != n:
        return "AMBIGUOUS"

    # Reconstruct the manuscript
    result = fragments[order[0]]
    for i in range(1, n):
        prev_fragment = fragments[order[i - 1]]
        curr_fragment = fragments[order[i]]
        overlap = overlap_length(prev_fragment, curr_fragment)
        result += curr_fragment[overlap:]

    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    n = int(data[0])
    fragments = data[1:n+1]
    
    result = find_optimal_reconstruction(fragments)
    print(result)

if __name__ == "__main__":
    main()