import sys
from collections import defaultdict, deque

def main():
    import sys
    from collections import defaultdict, deque

    def bfs(start, parent):
        queue = deque([start])
        depth = {start: 0}
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor != parent:
                    parent[neighbor] = node
                    depth[neighbor] = depth[node] + 1
                    queue.append(neighbor)
        return depth

    def find_farthest_node(start, parent):
        depth = bfs(start, parent)
        farthest_node = start
        max_depth = 0
        for node in depth:
            if depth[node] > max_depth:
                max_depth = depth[node]
                farthest_node = node
        return farthest_node, max_depth

    def find_diameter_and_path():
        parent = {}
        farthest_node, _ = find_farthest_node(1, parent)
        _, diameter = find_farthest_node(farthest_node, parent)
        return diameter, farthest_node

    def find_longest_path(start, parent):
        depth = bfs(start, parent)
        farthest_node, _ = find_farthest_node(start, parent)
        path = []
        current = farthest_node
        while current is not None:
            path.append(current)
            current = parent[current]
        return path

    def find_optimal_vertices():
        parent = {}
        _, farthest_node = find_farthest_node(1, parent)
        path = find_longest_path(farthest_node, parent)
        mid = len(path) // 2
        a = path[mid]
        b = path[0]
        c = path[-1]
        return a, b, c

    def calculate_result(a, b, c):
        path_ab = set()
        path_bc = set()
        path_ac = set()

        def add_path_edges(u, v, path_set):
            while u != v:
                path_set.add((u, v))
                u = parent[u]

        parent = {}
        bfs(a, parent)
        add_path_edges(b, a, path_ab)
        add_path_edges(c, a, path_ac)

        parent = {}
        bfs(b, parent)
        add_path_edges(c, b, path_bc)

        return len(path_ab.union(path_bc).union(path_ac))

    n = int(sys.stdin.readline())
    graph = defaultdict(list)
    for _ in range(n - 1):
        u, v = map(int, sys.stdin.readline().split())
        graph[u].append(v)
        graph[v].append(u)

    a, b, c = find_optimal_vertices()
    res = calculate_result(a, b, c)
    print(res)
    print(a, b, c)

if __name__ == "__main__":
    main()