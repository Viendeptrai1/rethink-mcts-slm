def find_max_participants(n, k, preferences):
    from collections import defaultdict, deque

    def find_scc(v, visited, stack, graph):
        visited[v] = True
        for neighbor in graph[v]:
            if not visited[neighbor]:
                find_scc(neighbor, visited, stack, graph)
        stack.append(v)

    def reverse_graph(graph, n):
        reversed_g = defaultdict(list)
        for v in range(1, n + 1):
            for neighbor in graph[v]:
                reversed_g[neighbor].append(v)
        return reversed_g

    def dfs(v, visited, graph):
        visited[v] = True
        for neighbor in graph[v]:
            if not visited[neighbor]:
                dfs(neighbor, visited, graph)

    # Step 1: Build the graph
    graph = defaultdict(list)
    for i in range(1, n + 1):
        graph[i].append(preferences[i - 1])

    # Step 2: Find all SCCs using Kosaraju's algorithm
    visited = [False] * (n + 1)
    stack = []

    for i in range(1, n + 1):
        if not visited[i]:
            find_scc(i, visited, stack, graph)

    # Step 3: Reverse the graph
    reversed_g = reverse_graph(graph, n)

    # Step 4: Process nodes in order of their finishing times
    visited = [False] * (n + 1)
    scc_count = 0

    while stack:
        v = stack.pop()
        if not visited[v]:
            dfs(v, visited, reversed_g)
            scc_count += 1

    # Step 5: Calculate the maximum number of participants that can join
    # Each SCC with more than one node can be considered as a single unit
    # Each SCC with exactly one node can be considered as a single unit
    # The maximum number of participants is the minimum of the number of SCCs and the bus capacity
    return min(scc_count, k)

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
preferences = list(map(int, data[2:]))

# Output the result
print(find_max_participants(n, k, preferences))