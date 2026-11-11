import sys
from collections import deque

def solve():
    import sys
    from collections import deque

    def read_ints():
        return list(map(int, sys.stdin.read().split()))

    n = read_ints()[0]
    a = read_ints()

    # Separate indices based on parity of a[i]
    odd_indices = [i for i in range(n) if a[i] % 2 == 1]
    even_indices = [i for i in range(n) if a[i] % 2 == 0]

    def bfs(start_indices):
        visited = [False] * n
        distance = [-1] * n
        queue = deque(start_indices)
        
        for start in start_indices:
            visited[start] = True
            distance[start] = 0
        
        while queue:
            current = queue.popleft()
            for next_pos in [current - a[current], current + a[current]]:
                if 0 <= next_pos < n and not visited[next_pos]:
                    visited[next_pos] = True
                    distance[next_pos] = distance[current] + 1
                    queue.append(next_pos)
        
        return distance

    odd_to_even = bfs(odd_indices)
    even_to_odd = bfs(even_indices)

    result = []
    for i in range(n):
        if a[i] % 2 == 1:
            result.append(even_to_odd[i])
        else:
            result.append(odd_to_even[i])

    print(" ".join(map(str, result)))

solve()