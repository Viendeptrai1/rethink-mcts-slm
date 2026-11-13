import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    if n == 1:
        print(0)
        return

    x = [0] * n
    y = [0] * n
    z = [0] * n

    for i in range(n):
        x[i] = int(next(iterator))
        y[i] = int(next(iterator))
        z[i] = int(next(iterator))

    edges = []

    # Sort by x and add edges between adjacent planets
    idx_x = sorted(range(n), key=lambda i: x[i])
    for i in range(n - 1):
        u = idx_x[i]
        v = idx_x[i + 1]
        edges.append((abs(x[u] - x[v]), u, v))

    # Sort by y and add edges between adjacent planets
    idx_y = sorted(range(n), key=lambda i: y[i])
    for i in range(n - 1):
        u = idx_y[i]
        v = idx_y[i + 1]
        edges.append((abs(y[u] - y[v]), u, v))

    # Sort by z and add edges between adjacent planets
    idx_z = sorted(range(n), key=lambda i: z[i])
    for i in range(n - 1):
        u = idx_z[i]
        v = idx_z[i + 1]
        edges.append((abs(z[u] - z[v]), u, v))

    # Kruskal's algorithm
    parent = list(range(n))
    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False

    edges.sort()
    mst_cost = 0
    edges_count = 0

    for cost, u, v in edges:
        if union(u, v):
            mst_cost += cost
            edges_count += 1
            if edges_count == n - 1:
                break

    print(mst_cost)

if __name__ == "__main__":
    solve()