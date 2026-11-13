from collections import deque

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    def bfs(start):
        queue = deque([(start, 0)])
        visited = set([start])
        while queue:
            pos, dist = queue.popleft()
            for next_pos in [pos - a[pos - 1], pos + a[pos - 1]]:
                if 1 <= next_pos <= n and next_pos not in visited:
                    if a[next_pos - 1] % 2 != a[start - 1] % 2:
                        return dist + 1
                    queue.append((next_pos, dist + 1))
                    visited.add(next_pos)
        return -1
    
    result = [bfs(i) for i in range(1, n + 1)]
    print(*result)

solve()