import sys
import math
from typing import List, Tuple

def distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def find_min_D(N: int, K: int, cities: List[Tuple[int, int, int]]) -> float:
    def can_form_happy_county(D: float) -> bool:
        def dfs(city_index: int, current_sum: int, visited: List[bool]) -> bool:
            if visited[city_index]:
                return False
            visited[city_index] = True
            current_sum += cities[city_index][2]
            if current_sum % K == 0:
                return True
            for neighbor in range(N):
                if not visited[neighbor] and distance(cities[city_index][:2], cities[neighbor][:2]) <= D:
                    if dfs(neighbor, current_sum, visited):
                        return True
            return False
        
        for start_city in range(N):
            visited = [False] * N
            if dfs(start_city, 0, visited):
                return True
        return False
    
    left, right = 0.0, 100000000.0
    while right - left > 1e-6:
        mid = (left + right) / 2
        if can_form_happy_county(mid):
            right = mid
        else:
            left = mid
    return round(left, 3)

def main():
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
    print(result)

if __name__ == "__main__":
    main()