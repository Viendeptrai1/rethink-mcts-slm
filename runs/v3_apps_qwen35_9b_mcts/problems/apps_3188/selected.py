import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    planets = []
    for i in range(n):
        x = int(next(iterator))
        y = int(next(iterator))
        z = int(next(iterator))
        planets.append((x, y, z))

    if n <= 1:
        print(0)
        return

    edges = []

    # Sort by x and add edges between adjacent planets
    sorted_by_x = sorted(range(n), key=lambda i: planets[i][0])
    for i in range(n - 1):
        u = sorted_by_x[i]
        v = sorted_by_x[i + 1]
        cost = min(abs(planets[u][0] - planets[v][0]),
                   abs(planets[u][1] - planets[v][1]),
                   abs(planets[u][2] - planets[v][2]))
        edges.append((cost, u, v))

    # Sort by y and add edges between adjacent planets
    sorted_by_y = sorted(range(n), key=lambda i: planets[i][1])
    for i in range(n - 1):
        u = sorted_by_y[i]
        v = sorted_by_y[i + 1]
        cost = min(abs(planets[u][0] - planets[v][0]),
                   abs(planets[u][1] - planets[v][1]),
                   abs(planets[u][2] - planets[v][2]))
        edges.append((cost, u, v))

    # Sort by z and add edges between adjacent planets
    sorted_by_z = sorted(range(n), key=lambda i: planets[i][2])
    for i in range(n - 1):
        u = sorted_by_z[i]
        v = sorted_by_z[i + 1]
        cost = min(abs(planets[u][0] - planets[v][0]),
                   abs(planets[u][1] - planets[v][1]),
                   abs(planets[u][2] - planets[v][2]))
        edges.append((cost, u, v))

    edges.sort(key=lambda x: x[0])

    parent = list(range(n))
    rank = [0] * n

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i == root_j:
            return False
        if rank[root_i] < rank[root_j]:
            parent[root_i] = root_j
        elif rank[root_i] > rank[root_j]:
            parent[root_j] = root_i
        else:
            parent[root_j] = root_i
            rank[root_i] += 1
        return True

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