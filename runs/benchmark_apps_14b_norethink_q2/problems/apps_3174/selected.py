import sys
import math
from collections import defaultdict, deque

def find_min_D(N, K, cities):
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def can_form_happy_subset(county):
        n = len(county)
        sums = [0] * (1 << n)
        for i in range(n):
            for mask in range(1 << i):
                sums[mask | (1 << i)] = (sums[mask] + county[i][2]) % K
        for mask in range(1, 1 << n):
            if sums[mask] == 0:
                return True
        return False

    def bfs_to_find_max_distance():
        max_dist = 0
        for i in range(N):
            visited = [False] * N
            queue = deque([(i, 0)])
            visited[i] = True
            while queue:
                u, dist = queue.popleft()
                for v in range(N):
                    if not visited[v]:
                        d = distance(cities[u], cities[v])
                        if d <= D:
                            visited[v] = True
                            queue.append((v, dist + d))
                            max_dist = max(max_dist, dist + d)
        return max_dist

    left, right = 0, 1000000000
    while right - left > 1e-6:
        mid = (left + right) / 2
        D = mid
        county = []
        visited = [False] * N
        for i in range(N):
            if not visited[i]:
                county.clear()
                queue = deque([i])
                visited[i] = True
                while queue:
                    u = queue.popleft()
                    county.append(cities[u])
                    for v in range(N):
                        if not visited[v] and distance(cities[u], cities[v]) <= D:
                            visited[v] = True
                            queue.append(v)
                if can_form_happy_subset(county):
                    right = mid
                    break
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