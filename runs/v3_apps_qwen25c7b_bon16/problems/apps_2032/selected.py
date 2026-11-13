import sys
from collections import defaultdict, deque

def max_defended_score(n, m, k, a, b, c, portals):
    graph = defaultdict(list)
    for u, v in portals:
        graph[u].append(v)

    def bfs(start):
        queue = deque([start])
        visited = set([start])
        distance = [float('inf')] * (n + 1)
        distance[start] = 0
        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    distance[neighbor] = distance[current] + 1
                    queue.append(neighbor)
        return distance

    def can_capture_all_castles():
        dp = [-1] * (n + 1)
        dp[0] = 0
        max_army = k
        for i in range(1, n + 1):
            if dp[i - 1] == -1:
                return False
            min_warriors_needed = a[i - 1]
            if max_army >= min_warriors_needed:
                dp[i] = dp[i - 1] + max(c[i - 1], 0)
                max_army += b[i - 1]
                distances = bfs(i)
                for j in range(i + 1, n + 1):
                    if distances[j] != float('inf') and max_army - distances[j] >= a[j - 1]:
                        dp[j] = max(dp[j], dp[i] - (distances[j] - 1))
                        max_army -= distances[j] - 1
        return dp[n]

    return can_capture_all_castles()

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    
    a = []
    b = []
    c = []
    for i in range(n):
        a.append(int(data[3 + 3 * i]))
        b.append(int(data[4 + 3 * i]))
        c.append(int(data[5 + 3 * i]))
    
    portals = []
    for i in range(m):
        portals.append((int(data[6 + 6 * i]) - 1, int(data[7 + 6 * i]) - 1))
    
    result = max_defended_score(n, m, k, a, b, c, portals)
    print(result)