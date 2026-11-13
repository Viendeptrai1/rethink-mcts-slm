import sys
from math import sqrt
from collections import defaultdict

def find_minimal_d(N, K, cities):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    def bfs(start, max_distance):
        visited = [False] * N
        queue = [(start, 0)]
        visited[start] = True
        while queue:
            current, distance = queue.pop(0)
            if distance > max_distance:
                break
            for neighbor, dist in graph[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, distance + dist))
        return any(residents[i] % K == 0 for i in range(N) if visited[i])

    graph = defaultdict(list)
    residents = [city[2] for city in cities]
    for i in range(N):
        for j in range(i + 1, N):
            dx, dy = cities[i][0] - cities[j][0], cities[i][1] - cities[j][1]
            d = sqrt(dx**2 + dy**2)
            if d <= D:
                graph[i].append((j, d))
                graph[j].append((i, d))

    left, right = 0, float('inf')
    while right - left > 1e-6:
        mid = (left + right) / 2
        if bfs(0, mid):
            right = mid
        else:
            left = mid

    return round(right, 3)

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
        cities.append((x, y, k))
        index += 3

    result = find_minimal_d(N, K, cities)
    print(result)