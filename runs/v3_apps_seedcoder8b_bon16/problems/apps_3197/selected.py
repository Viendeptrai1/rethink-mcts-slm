def solve_trip(n, k, preferences):
    def dfs(node, visited, stack):
        visited[node] = True
        stack[node] = True
        for neighbor in graph[node]:
            if stack[neighbor]:
                return True
            if not visited[neighbor]:
                if dfs(neighbor, visited, stack):
                    return True
        stack[node] = False
        return False

    def find_cycle():
        visited = [False] * (n + 1)
        stack = [False] * (n + 1)
        for i in range(1, n + 1):
            if not visited[i]:
                if dfs(i, visited, stack):
                    return True
        return False

    graph = [[] for _ in range(n + 1)]
    for i, pref in enumerate(preferences, 1):
        graph[i].append(pref)

    if find_cycle():
        return k

    def dfs_count(node, visited):
        visited[node] = True
        count = 1
        for neighbor in graph[node]:
            if not visited[neighbor]:
                count += dfs_count(neighbor, visited)
        return count

    visited = [False] * (n + 1)
    component_sizes = []
    for i in range(1, n + 1):
        if not visited[i]:
            component_sizes.append(dfs_count(i, visited))

    component_sizes.sort(reverse=True)
    return sum(component_sizes[:k])

n, k = map(int, input().split())
preferences = list(map(int, input().split()))
print(solve_trip(n, k, preferences))