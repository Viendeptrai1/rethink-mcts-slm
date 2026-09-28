import sys
from collections import defaultdict, deque

def dfs(node, parent, graph):
    max_depth = 0
    farthest_node = node
    for neighbor in graph[node]:
        if neighbor != parent:
            depth, farthest = dfs(neighbor, node, graph)
            if depth + 1 > max_depth:
                max_depth = depth + 1
                farthest_node = farthest
    return max_depth, farthest_node

def find_diameter(graph, n):
    _, first_end = dfs(1, -1, graph)
    _, second_end = dfs(first_end, -1, graph)
    return first_end, second_end

def bfs(start, graph, n):
    queue = deque([(start, 0)])
    distances = [-1] * (n + 1)
    distances[start] = 0
    while queue:
        node, dist = queue.popleft()
        for neighbor in graph[node]:
            if distances[neighbor] == -1:
                distances[neighbor] = dist + 1
                queue.append((neighbor, dist + 1))
    return distances

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    graph = defaultdict(list)
    index = 1
    for _ in range(n - 1):
        a = int(data[index])
        b = int(data[index + 1])
        graph[a].append(b)
        graph[b].append(a)
        index += 2
    
    first_end, second_end = find_diameter(graph, n)
    distances_from_first = bfs(first_end, graph, n)
    distances_from_second = bfs(second_end, graph, n)
    
    max_covered_edges = 0
    best_a, best_b, best_c = -1, -1, -1
    
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            for k in range(j + 1, n + 1):
                covered_edges = set()
                for node in [i, j, k]:
                    covered_edges.update(graph[node])
                covered_edges.discard(i)
                covered_edges.discard(j)
                covered_edges.discard(k)
                if len(covered_edges) > max_covered_edges:
                    max_covered_edges = len(covered_edges)
                    best_a, best_b, best_c = i, j, k
    
    print(max_covered_edges)
    print(best_a, best_b, best_c)

if __name__ == "__main__":
    main()