import sys
from heapq import heappop, heappush
from math import sqrt

def find(parent, i):
    if parent[i] == i:
        return i
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

def kruskal(graph, n, k):
    result = []
    i = e = 0
    graph.sort(key=lambda item: item[2])
    parent = list(range(n))
    rank = [0] * n

    while e < n - 1:
        u, v, w = graph[i]
        i += 1
        x = find(parent, u)
        y = find(parent, v)

        if x != y:
            e += 1
            result.append([u, v, w])
            union(parent, rank, x, y)

    min_d = float('inf')
    for u, v, w in result:
        if w <= min_d:
            min_d = w

    return min_d

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    k = int(data[index + 1])
    index += 2
    
    cities = []
    for _ in range(n):
        x = int(data[index])
        y = int(data[index + 1])
        k_i = int(data[index + 2])
        index += 3
        cities.append((x, y, k_i))

    graph = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = sqrt((cities[i][0] - cities[j][0]) ** 2 + (cities[i][1] - cities[j][1]) ** 2)
            graph.append((i, j, dist))

    min_d = kruskal(graph, n, k)
    print(f"{min_d:.3f}")

if __name__ == "__main__":
    main()