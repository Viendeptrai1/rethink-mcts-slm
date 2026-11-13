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

    # BFS to find minimum swaps
    # State is a tuple of the current permutation
    start_state = tuple(initial_perm)
    if start_state == target:
        print(0)
        return

    queue = deque([(start_state, 0)])
    visited = {start_state}

    while queue:
        current, dist = queue.popleft()

        # Try all allowed swaps
        for u, v in swaps:
            # Create new state by swapping elements at indices u and v
            new_list = list(current)
            new_list[u], new_list[v] = new_list[v], new_list[u]
            new_state = tuple(new_list)

            if new_state == target:
                print(dist + 1)
                return

            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, dist + 1))

if __name__ == "__main__":
    solve()