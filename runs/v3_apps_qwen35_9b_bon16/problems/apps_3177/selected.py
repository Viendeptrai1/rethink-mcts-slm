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
        
        initial_perm = [0] * N
        for i in range(N):
            initial_perm[i] = int(next(iterator)) - 1  # Convert to 0-based
        
        swaps = set()
        for _ in range(M):
            a = int(next(iterator)) - 1
            b = int(next(iterator)) - 1
            if a > b:
                a, b = b, a
            swaps.add((a, b))
            
    except StopIteration:
        return

    # Target is sorted: 0, 1, 2, ..., N-1
    target = tuple(range(N))
    current = tuple(initial_perm)
    
    if current == target:
        print(0)
        return

    # BFS to find minimum swaps
    queue = deque()
    queue.append((current, 0))
    visited = {current}
    
    while queue:
        state, steps = queue.popleft()
        
        # Generate all possible next states
        next_states = []
        for (a, b) in swaps:
            lst = list(state)
            lst[a], lst[b] = lst[b], lst[a]
            next_states.append(tuple(lst))
        
        for next_state in next_states:
            if next_state == target:
                print(steps + 1)
                return
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps + 1))

if __name__ == "__main__":
    solve()