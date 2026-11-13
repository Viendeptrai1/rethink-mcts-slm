import sys
from collections import defaultdict

def count_valid_paintings(N, edges, M, restrictions):
    # Helper function to find the path between two nodes using DFS
    def find_path(graph, start, end, path):
        path.append(start)
        if start == end:
            return True
        for neighbor in graph[start]:
            if neighbor not in path:
                if find_path(graph, neighbor, end, path):
                    return True
        path.pop()
        return False

    # Build the graph from edges
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # Check if a path between u and v contains at least one black edge
    def path_contains_black_edge(u, v, black_edges):
        path = []
        find_path(graph, u, v, path)
        for i in range(len(path) - 1):
            if (path[i], path[i + 1]) in black_edges or (path[i + 1], path[i]) in black_edges:
                return True
        return False

    # Total number of ways to paint the edges
    total_ways = 1 << (N - 1)
    invalid_ways = 0

    # Iterate over all possible sets of black edges
    for mask in range(1 << (N - 1)):
        black_edges = set()
        edge_index = 0
        for i in range(1, N):
            for j in range(i + 1, N + 1):
                if (edges[edge_index][0] == i and edges[edge_index][1] == j) or (edges[edge_index][0] == j and edges[edge_index][1] == i):
                    if mask & (1 << edge_index):
                        black_edges.add((i, j))
                    break
                edge_index += 1

        # Check if this set of black edges satisfies all restrictions
        valid = True
        for u, v in restrictions:
            if not path_contains_black_edge(u, v, black_edges):
                valid = False
                break

        if not valid:
            invalid_ways += 1

    # Return the number of valid ways
    return total_ways - invalid_ways

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    
    edges = []
    for _ in range(N - 1):
        a = int(data[index])
        b = int(data[index + 1])
        edges.append((a, b))
        index += 2
    
    M = int(data[index])
    index += 1
    
    restrictions = []
    for _ in range(M):
        u = int(data[index])
        v = int(data[index + 1])
        restrictions.append((u, v))
        index += 2
    
    result = count_valid_paintings(N, edges, M, restrictions)
    print(result)

if __name__ == "__main__":
    main()