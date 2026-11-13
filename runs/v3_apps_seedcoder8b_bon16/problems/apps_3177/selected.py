def minimum_swaps_to_sort(N, M, initial_permutation, allowed_swaps):
    from collections import defaultdict, deque

    # Helper function to find the minimum swaps needed
    def min_swaps_to_sort(permutation):
        # Create a list of tuples where each tuple is (value, index)
        array_pos = [(value, idx) for idx, value in enumerate(permutation)]
        # Sort the array by the values
        array_pos.sort()
        # To keep track of visited elements
        visited = {k: False for k in range(N)}

        swaps = 0
        for i in range(N):
            # If element is visited or already in the correct position
            if visited[i] or array_pos[i][1] == i:
                continue

            # Calculate number of nodes in this cycle
            cycle_size = 0
            j = i

            while not visited[j]:
                visited[j] = True
                j = array_pos[j][1]
                cycle_size += 1

            if cycle_size > 0:
                swaps += (cycle_size - 1)

        return swaps

    # Generate the graph of allowed swaps
    graph = defaultdict(list)
    for A, B in allowed_swaps:
        graph[A - 1].append(B - 1)
        graph[B - 1].append(A - 1)

    # BFS to determine the connected components
    def bfs(start):
        queue = deque([start])
        component = []
        visited[start] = True
        while queue:
            node = queue.popleft()
            component.append(node)
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        return component

    visited = [False] * N
    components = []
    for i in range(N):
        if not visited[i]:
            components.append(bfs(i))

    # Check if all components are already in sorted order
    min_swaps = 0
    for component in components:
        permutation_slice = [initial_permutation[i] for i in component]
        min_swaps += min_swaps_to_sort(permutation_slice)

    return min_swaps

import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])
initial_permutation = list(map(int, data[2:N+2]))
allowed_swaps = []
index = N + 2
for _ in range(M):
    A = int(data[index])
    B = int(data[index + 1])
    allowed_swaps.append((A, B))
    index += 2

print(minimum_swaps_to_sort(N, M, initial_permutation, allowed_swaps))