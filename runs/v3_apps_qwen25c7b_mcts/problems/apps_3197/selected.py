def max_participants(n, k, preferences):
    parent = list(range(n + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            parent[rootX] = rootY
    
    for i in range(1, n + 1):
        union(i, preferences[i - 1])
    
    groups = {}
    for i in range(1, n + 1):
        root = find(i)
        if root not in groups:
            groups[root] = 0
        groups[root] += 1
    
    return min(sum(groups.values()), k)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
preferences = list(map(int, data[2:]))

print(max_participants(n, k, preferences))