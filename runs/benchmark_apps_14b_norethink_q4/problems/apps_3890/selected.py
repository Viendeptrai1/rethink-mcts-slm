MOD = 1000000007

def count_ways(n, k):
    def dfs(node, visited, stack, graph, component):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, visited, stack, graph, component)
        stack.append(node)

    def reverse_dfs(node, visited, graph, component):
        visited[node] = True
        component.append(node)
        for neighbor in graph[node]:
            if not visited[neighbor]:
                reverse_dfs(neighbor, visited, graph, component)

    # Step 1: Create the graph
    graph = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        graph[i].append(i)  # Self-loop for every node

    # Step 2: Perform DFS to fill the stack
    visited = [False] * (n + 1)
    stack = []
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i, visited, stack, graph, [])

    # Step 3: Reverse the graph
    reversed_graph = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for neighbor in graph[i]:
            reversed_graph[neighbor].append(i)

    # Step 4: Perform DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    sccs = []
    while stack:
        node = stack.pop()
        if not visited[node]:
            component = []
            reverse_dfs(node, visited, reversed_graph, component)
            sccs.append(component)

    # Step 5: Count valid configurations
    def count_permutations(size):
        return pow(size, size, MOD)

    result = 1
    for scc in sccs:
        if 1 in scc:
            if len(scc) <= k:
                result = (result * count_permutations(len(scc))) % MOD
        else:
            if len(scc) > k:
                result = (result * count_permutations(len(scc))) % MOD

    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Output the result
print(count_ways(n, k))