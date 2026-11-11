import sys
from collections import defaultdict, deque

def main():
    import sys
    import threading
    def compute_subtree_sizes(tree):
        sizes = {}
        def dfs(node):
            size = 1
            for child in tree[node]:
                size += dfs(child)
            sizes[node] = size
            return size
        dfs(1)
        return sizes

    def preprocess_lca(tree, n):
        levels = [0] * (n + 1)
        parents = [[0] * 18 for _ in range(n + 1)]
        
        def dfs(node, level):
            levels[node] = level
            for child in tree[node]:
                parents[child][0] = node
                dfs(child, level + 1)
        
        dfs(1, 0)
        
        for j in range(1, 18):
            for i in range(1, n + 1):
                parents[i][j] = parents[parents[i][j - 1]][j - 1]
        
        return levels, parents

    def lca(u, v, levels, parents):
        if levels[u] < levels[v]:
            u, v = v, u
        diff = levels[u] - levels[v]
        for i in range(18):
            if diff & (1 << i):
                u = parents[u][i]
        if u == v:
            return u
        for i in range(17, -1, -1):
            if parents[u][i] != parents[v][i]:
                u = parents[u][i]
                v = parents[v][i]
        return parents[u][0]

    def dfs_order(tree, n):
        order = []
        visited = [False] * (n + 1)
        
        def dfs(node):
            visited[node] = True
            order.append(node)
            for child in tree[node]:
                if not visited[child]:
                    dfs(child)
            order.append(node)
        
        dfs(1)
        return order

    def solve_query(u, k, order, subtree_sizes, levels, parents):
        start_index = order.index(u)
        end_index = start_index + subtree_sizes[u] - 1
        
        if k > subtree_sizes[u]:
            return -1
        
        current_node = u
        current_level = levels[u]
        
        while k > 1:
            max_jump = 0
            for i in range(18):
                if levels[current_node] - (1 << i) >= current_level - k + 1:
                    max_jump = i
            current_node = parents[current_node][max_jump]
            k -= (1 << max_jump)
        
        return current_node

    def read_input():
        import sys
        data = sys.stdin.read().split()
        index = 0
        n = int(data[index])
        q = int(data[index + 1])
        index += 2
        tree = defaultdict(list)
        for i in range(2, n + 1):
            parent = int(data[index + i - 2])
            tree[parent].append(i)
        index += n - 1
        queries = []
        for _ in range(q):
            u = int(data[index])
            k = int(data[index + 1])
            queries.append((u, k))
            index += 2
        return n, q, tree, queries

    def write_output(results):
        for result in results:
            print(result)

    n, q, tree, queries = read_input()
    subtree_sizes = compute_subtree_sizes(tree)
    levels, parents = preprocess_lca(tree, n)
    order = dfs_order(tree, n)
    results = []
    for u, k in queries:
        result = solve_query(u, k, order, subtree_sizes, levels, parents)
        results.append(result)
    write_output(results)

threading.Thread(target=main).start()