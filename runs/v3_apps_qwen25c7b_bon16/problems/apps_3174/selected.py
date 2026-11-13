import sys
from typing import List
from math import sqrt
from collections import defaultdict

def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

def find(parent: List[int], u: int) -> int:
    if parent[u] != u:
        parent[u] = find(parent, parent[u])
    return parent[u]

def union(parent: List[int], rank: List[int], u: int, v: int) -> None:
    root_u = find(parent, u)
    root_v = find(parent, v)
    if root_u != root_v:
        if rank[root_u] > rank[root_v]:
            parent[root_v] = root_u
        elif rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        else:
            parent[root_v] = root_u
            rank[root_u] += 1

def minimum_diameter(N: int, K: int, cities: List[List[int]]) -> float:
    edges = []
    for i in range(N):
        x1, y1, _ = cities[i]
        for j in range(i + 1, N):
            x2, y2, _ = cities[j]
            d = sqrt((x2 - x1)**2 + (y2 - y1)**2)
            edges.append((d, i, j))
    
    edges.sort()
    
    parent = list(range(N))
    rank = [0] * N
    
    min_diameter = 0
    added_edges = set()
    
    for d, u, v in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            added_edges.add((u, v))
            min_diameter = max(min_diameter, d)
    
    # Check for the condition where there exists a subset of cities with residents sum divisible by K
    subsets = defaultdict(list)
    for i in range(N):
        root = find(parent, i)
        subsets[root].append(cities[i][2])
    
    for subset in subsets.values():
        current_sum = 0
        gcd_value = 0
        for residents in subset:
            current_sum += residents
            gcd_value = gcd(gcd_value, residents)
        if current_sum % K == 0 or gcd_value > 0:
            break
    
    return round(min_diameter, 3)

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    index = 0
    
    N = int(data[index])
    K = int(data[index + 1])
    index += 2
    
    cities = []
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        k = int(data[index + 2])
        index += 3
        cities.append([x, y, k])
    
    result = minimum_diameter(N, K, cities)
    print(result)