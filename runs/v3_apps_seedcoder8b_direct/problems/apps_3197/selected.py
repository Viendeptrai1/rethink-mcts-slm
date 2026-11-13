def find_max_participants(n, k, preferences):
    from collections import defaultdict, deque

    # Create a graph where each node points to the node it prefers
    graph = defaultdict(list)
    in_degree = [0] * (n + 1)

    for i in range(n):
        preferred = preferences[i]
        graph[preferred].append(i + 1)
        in_degree[i + 1] += 1

    # Find all nodes with no incoming edges (i.e., they are not preferred by anyone else)
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)

    # Perform a topological sort
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # The maximum number of participants that can join is the minimum of visited nodes and bus capacity
    return min(visited, k)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    preferences = list(map(int, data[2:]))
    
    result = find_max_participants(n, k, preferences)
    print(result)