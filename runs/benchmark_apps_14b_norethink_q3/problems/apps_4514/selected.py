import sys
from collections import defaultdict

def main():
    import sys
    import threading
    def compute_dfs_order(n, edges):
        from collections import deque
        adj_list = defaultdict(list)
        for v, u in enumerate(edges, start=1):
            adj_list[u].append(v)
        
        def dfs(node, parent):
            order.append(node)
            for neighbor in adj_list[node]:
                if neighbor != parent:
                    dfs(neighbor, node)
        
        order = []
        dfs(1, -1)
        return order

    def solve(n, q, edges, queries):
        dfs_order = compute_dfs_order(n, edges)
        results = []
        for u, k in queries:
            if k > len(dfs_order):
                results.append(-1)
            else:
                results.append(dfs_order[k-1])
        return results

    def read_input():
        import sys
        data = sys.stdin.read().split()
        n = int(data[0])
        q = int(data[1])
        edges = list(map(int, data[2:n+1]))
        queries = []
        for i in range(q):
            u = int(data[n+1 + 2*i])
            k = int(data[n+2 + 2*i])
            queries.append((u, k))
        return n, q, edges, queries

    def write_output(results):
        print("\n".join(map(str, results)))

    n, q, edges, queries = read_input()
    results = solve(n, q, edges, queries)
    write_output(results)

if __name__ == "__main__":
    threading.Thread(target=main).start()