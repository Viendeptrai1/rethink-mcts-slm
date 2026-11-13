import sys
import math
from collections import defaultdict

def find(parent, i):
    if parent[i] == i:
        return i
    else:
        return find(parent, parent[i])

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

def calculate_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def can_form_happy_county(county_residents, K):
    n = len(county_residents)
    prefix_sums = {0}
    current_sum = 0
    
    for r in county_residents:
        current_sum += r
        remainder = current_sum % K
        if remainder in prefix_sums:
            return True
        prefix_sums.add(remainder)
    
    return False

def minimal_D_for_happy_county(N, K, cities):
    edges = []
    
    for i in range(N):
        for j in range(i + 1, N):
            distance = calculate_distance(cities[i][:2], cities[j][:2])
            if distance <= 100000000:  # Avoid unnecessary large distances
                edges.append((distance, i, j))
    
    edges.sort()
    
    parent = list(range(N))
    rank = [0] * N
    
    for distance, u, v in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
        
        # Check if we can form a happy county
        county_map = defaultdict(list)
        for city in range(N):
            root = find(parent, city)
            county_map[root].append(cities[city][2])
        
        for county_residents in county_map.values():
            if can_form_happy_county(county_residents, K):
                return f"{distance:.3f}"
    
    return "UNSOLVABLE##"

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
    
    result = minimal_D_for_happy_county(N, K, cities)
    print(result)

if __name__ == "__main__":
    main()