import sys
import math
from collections import defaultdict, deque

def find(parent, i):
    if parent[i] == i:
        return i
    else:
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

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def can_be_happy(N, K, cities, D):
    parent = list(range(N))
    rank = [0] * N
    edges = []

    for i in range(N):
        for j in range(i + 1, N):
            dist = distance(cities[i], cities[j])
            if dist <= D:
                edges.append((dist, i, j))

    edges.sort()

    for dist, u, v in edges:
        union(parent, rank, u, v)

    components = defaultdict(list)
    for i in range(N):
        root = find(parent, i)
        components[root].append(i)

    for component in components.values():
        subset_sums = [0] * K
        subset_sums[0] = 1
        current_sum = 0
        for city in component:
            current_sum = (current_sum + cities[city][2]) % K
            if subset_sums[current_sum]:
                return True
            subset_sums[current_sum] = 1
        subset_sums = [0] * K
        subset_sums[0] = 1
        current_sum = 0
        for city in reversed(component):
            current_sum = (current_sum + cities[city][2]) % K
            if subset_sums[current_sum]:
                return True
            subset_sums[current_sum] = 1

    return False

def minimal_D(N, K, cities):
    low, high = 0, 1e7
    while high - low > 1e-6:
        mid = (low + high) / 2
        if can_be_happy(N, K, cities, mid):
            high = mid
        else:
            low = mid
    return high

def main():
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    cities = []
    index = 2
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        k = int(data[index + 2])
        cities.append((x, y, k))
        index += 3
    result = minimal_D(N, K, cities)
    print(f"{result:.3f}")

if __name__ == "__main__":
    main()