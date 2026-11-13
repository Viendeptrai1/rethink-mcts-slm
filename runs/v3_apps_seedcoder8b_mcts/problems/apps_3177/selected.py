from collections import deque

def min_swaps_to_sort(N, M, permutation, allowed_swaps):
    # Convert the permutation to a tuple for immutability in the queue
    target = tuple(range(1, N + 1))
    start = tuple(permutation)
    
    # Create a graph of allowed swaps
    graph = {i: [] for i in range(1, N + 1)}
    for a, b in allowed_swaps:
        graph[a].append(b)
        graph[b].append(a)
    
    # BFS setup
    queue = deque([(start, 0)])  # (current permutation, number of swaps)
    visited = set([start])
    
    while queue:
        current, swaps = queue.popleft()
        
        if current == target:
            return swaps
        
        # Try all possible swaps
        for i in range(1, N + 1):
            for j in graph[i]:
                if i < j:  # Avoid duplicate swaps
                    new_perm = list(current)
                    new_perm[i - 1], new_perm[j - 1] = new_perm[j - 1], new_perm[i - 1]
                    new_perm_tuple = tuple(new_perm)
                    
                    if new_perm_tuple not in visited:
                        visited.add(new_perm_tuple)
                        queue.append((new_perm_tuple, swaps + 1))
    
    return -1  # Should never reach here if a solution exists

# Read input
N, M = map(int, input().split())
permutation = list(map(int, input().split()))
allowed_swaps = [tuple(map(int, input().split())) for _ in range(M)]

# Solve and print result
result = min_swaps_to_sort(N, M, permutation, allowed_swaps)
print(result)