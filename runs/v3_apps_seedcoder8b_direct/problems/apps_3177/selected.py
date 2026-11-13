def minimum_swaps_to_sort(N, M, permutation, allowed_swaps):
    from collections import defaultdict, deque

    # Helper function to find the root of an element in the union-find structure
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    # Helper function to union two sets in the union-find structure
    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            parent[rootY] = rootX

    # Initialize union-find structure
    parent = list(range(N + 1))

    # Apply allowed swaps to union-find structure
    for a, b in allowed_swaps:
        union(a, b)

    # Group elements by their root in the union-find structure
    groups = defaultdict(list)
    for i in range(1, N + 1):
        root = find(i)
        groups[root].append(i)

    # Calculate the minimum number of swaps needed
    swaps = 0
    for group in groups.values():
        # Sort the group and the corresponding positions in the permutation
        sorted_group = sorted(group)
        current_positions = sorted((permutation.index(x), x) for x in group)

        # Calculate the number of misplaced elements
        misplaced = sum(1 for (pos, _), correct in zip(current_positions, sorted_group) if pos != correct)

        # Each swap fixes two misplaced elements
        swaps += misplaced // 2

    return swaps

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])
permutation = list(map(int, data[2:N+2]))
allowed_swaps = [(int(data[i]), int(data[i+1])) for i in range(N+2, len(data), 2)]

# Get the result
result = minimum_swaps_to_sort(N, M, permutation, allowed_swaps)

# Print the result
print(result)