import sys
import math
from typing import List, Tuple

def distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def can_form_happy_county(cities: List[Tuple[int, int, int]], D: float, K: int) -> bool:
    n = len(cities)
    parent = list(range(n))
    
    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x: int, y: int) -> None:
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            parent[rootX] = rootY
    
    for i in range(n):
        for j in range(i + 1, n):
            if distance(cities[i][:2], cities[j][:2]) <= D:
                union(i, j)
    
    county_sums = {}
    for i in range(n):
        root = find(i)
        if root not in county_sums:
            county_sums[root] = 0
        county_sums[root] += cities[i][2]
    
    for county_sum in county_sums.values():
        if county_sum % K == 0:
            return True
    
    return False

def find_min_D(N: int, K: int, cities: List[Tuple[int, int, int]]) -> float:
    max_dist = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            max_dist = max(max_dist, distance(cities[i][:2], cities[j][:2]))
    
    low, high = 0.0, max_dist
    while high - low > 1e-6:
        mid = (low + high) / 2
        if can_form_happy_county(cities, mid, K):
            high = mid
        else:
            low = mid
    
    return low

def main() -> None:
    import sys
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
    
    result = find_min_D(N, K, cities)
    print(f"{result:.3f}")

if __name__ == "__main__":
    main()