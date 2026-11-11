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

        # Check if it's possible to connect all districts without revolts
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
                if gangs[i] != gangs[j] and union(i, j):
                    edges.append((i + 1, j + 1))

        if len(edges) == n - 1:
            results.append("YES")
            results.extend(f"{x} {y}" for x, y in edges)
        else:
            results.append("NO")

    for result in results:
        print(result)

if __name__ == "__main__":
    solve()