import sys
input = sys.stdin.read
data = input().split()

def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i])
    return parent[i]

def union(parent, rank, x, y):
    rootX = find(parent, x)
    rootY = find(parent, y)
    
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

def solve():
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        gangs = list(map(int, data[index:index+n]))
        index += n
        
        parent = list(range(n))
        rank = [0] * n
        edges = []
        
        for i in range(n):
            for j in range(i+1, n):
                if gangs[i] != gangs[j]:
                    edges.append((i, j))
        
        mst = []
        for u, v in edges:
            if union(parent, rank, u, v):
                mst.append((u+1, v+1))
        
        if len(mst) == n-1:
            results.append("YES")
            results.extend(f"{u} {v}" for u, v in mst)
        else:
            results.append("NO")
    
    print("\n".join(results))

solve()