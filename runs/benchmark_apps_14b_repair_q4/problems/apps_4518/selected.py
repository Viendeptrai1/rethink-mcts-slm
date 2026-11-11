import sys
import random

def solve():
    import sys
    import random

    def readints():
        return list(map(int, sys.stdin.readline().split()))

    t = readints()[0]
    results = []

    for _ in range(t):
        n = readints()[0]
        gangs = readints()

        # Check if it's possible to connect all districts without any two districts of the same gang being directly connected
        unique_gangs = set(gangs)
        if len(unique_gangs) < n - 1:
            results.append("NO")
            continue

        # Create a spanning tree
        edges = []
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                if rank[rootX] > rank[rootY]:
                    parent[rootY] = rootX
                elif rank[rootX] < rank[rootY]:
                    parent[rootX] = rootY
                else:
                    parent[rootY] = rootX
                    rank[rootX] += 1
                return True
            return False

        for i in range(n):
            for j in range(i + 1, n):
                if gangs[i] != gangs[j]:
                    if union(i, j):
                        edges.append((i + 1, j + 1))

        # Check if we have a valid spanning tree
        if len(edges) == n - 1:
            results.append("YES")
            for edge in edges:
                results.append(f"{edge[0]} {edge[1]}")
        else:
            results.append("NO")

    for result in results:
        print(result)

if __name__ == "__main__":
    solve()