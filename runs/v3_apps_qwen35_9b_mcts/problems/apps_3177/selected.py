import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    initial_perm = []
    for _ in range(N):
        initial_perm.append(int(next(iterator)) - 1)  # Convert to 0-based

    swaps = []
    for _ in range(M):
        u = int(next(iterator)) - 1
        v = int(next(iterator)) - 1
        swaps.append((u, v))

    target = list(range(N))

    # BFS initialization
    queue = deque()
    queue.append(initial_perm)
    visited = {tuple(initial_perm): 0}

    while queue:
        current = queue.popleft()
        dist = visited[tuple(current)]

        if current == target:
            print(dist)
            return

        # Try all allowed swaps
        for u, v in swaps:
            # Create new permutation by swapping elements at indices u and v
            new_perm = list(current)
            new_perm[u], new_perm[v] = new_perm[v], new_perm[u]
            state = tuple(new_perm)

            if state not in visited:
                visited[state] = dist + 1
                queue.append(new_perm)

if __name__ == "__main__":
    solve()