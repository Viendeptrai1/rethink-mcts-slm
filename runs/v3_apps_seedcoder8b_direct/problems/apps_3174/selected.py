import sys
import math
from collections import defaultdict, deque

def minimal_d_for_happiness(N, K, cities):
    def distance(city1, city2):
        return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

    def can_form_county_with_happiness(d):
        adj = defaultdict(list)
        for i in range(N):
            for j in range(i + 1, N):
                if distance(cities[i], cities[j]) <= d:
                    adj[i].append(j)
                    adj[j].append(i)

        visited = [False] * N
        for start in range(N):
            if not visited[start]:
                queue = deque([start])
                visited[start] = True
                residents = [cities[start][2]]
                while queue:
                    city = queue.popleft()
                    for neighbor in adj[city]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
                            residents.append(cities[neighbor][2])

                # Check if there's a subset with sum divisible by K
                subset_sum = [0]
                for resident in residents:
                    new_sums = []
                    for s in subset_sum:
                        new_sums.append(s + resident)
                    subset_sum.extend(new_sums)
                    if any(s % K == 0 for s in subset_sum):
                        return True
        return False

    # Binary search for the minimal D
    low, high = 0, 1e7
    while high - low > 1e-6:
        mid = (low + high) / 2
        if can_form_county_with_happiness(mid):
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

    result = minimal_d_for_happiness(N, K, cities)
    print(f"{result:.3f}")

if __name__ == "__main__":
    main()