import sys
import heapq
from collections import defaultdict

def find(parent, i):
    if parent[i] == i:
        return i
    else:
        return find(parent, parent[i])

def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

def kruskal(n, edges):
    result = []
    i, e = 0, 0
    edges = sorted(edges, key=lambda item: item[2])
    parent = []
    rank = []

    for node in range(n):
        parent.append(node)
        rank.append(0)

    while e < n - 1:
        u, v, w = edges[i]
        i += 1
        x = find(parent, u)
        y = find(parent, v)

        if x != y:
            e += 1
            result.append((u, v, w))
            union(parent, rank, x, y)

    return result

def maximize_good_vertices(n, m, k, edges):
    edges_with_index = [(x-1, y-1, w, i+1) for i, (x, y, w) in enumerate(edges)]
    mst_edges = kruskal(n, [(x, y, w) for x, y, w, _ in edges_with_index])
    mst_edges_with_index = [(x, y, w, i) for (x, y, w), (_, _, _, i) in zip(mst_edges, edges_with_index)]

    if len(mst_edges_with_index) <= k:
        return len(mst_edges_with_index), [idx for _, _, _, idx in mst_edges_with_index]

    mst_edges_with_index.sort(key=lambda item: item[2], reverse=True)
    extra_edges = mst_edges_with_index[k:]
    remaining_edges = mst_edges_with_index[:k]

    remaining_edges_set = set((min(u, v), max(u, v)) for u, v, _, _ in remaining_edges)
    good_vertices = set()

    for u in range(n):
        if (0, u) in remaining_edges_set:
            good_vertices.add(u)

    for u, v, w, idx in extra_edges:
        if (min(u, v), max(u, v)) not in remaining_edges_set:
            good_vertices.add(u)
            good_vertices.add(v)

    return k, [idx for _, _, _, idx in remaining_edges]

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    
    edges = []
    index = 3
    for _ in range(m):
        x = int(data[index])
        y = int(data[index + 1])
        w = int(data[index + 2])
        edges.append((x, y, w))
        index += 3
    
    e, edge_indices = maximize_good_vertices(n, m, k, edges)
    print(e)
    print(' '.join(map(str, edge_indices)))

if __name__ == "__main__":
    main()