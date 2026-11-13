import sys
from collections import defaultdict, deque

def expected_time_to_exit(N, M, paths):
    # Create an adjacency list for the graph
    graph = defaultdict(list)
    for K, L in paths:
        graph[K].append(L)
        graph[L].append(K)

    # BFS to calculate the shortest path distances from the start to all nodes
    distances = [-1] * N
    distances[0] = 0
    queue = deque([0])

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if distances[neighbor] == -1:  # If not visited
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    # Calculate expected time to exit
    def dfs(node, visited):
        if node == N - 1:
            return 0
        visited.add(node)
        total_time = 0
        count = 0
        for neighbor in graph[node]:
            if neighbor not in visited:
                total_time += dfs(neighbor, visited)
                count += 1
        visited.remove(node)
        return (total_time + count) / count if count > 0 else float('inf')

    expected_time = dfs(0, set())
    return expected_time

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    paths = []
    
    index = 2
    for _ in range(M):
        K = int(data[index])
        L = int(data[index + 1])
        paths.append((K, L))
        index += 2
    
    result = expected_time_to_exit(N, M, paths)
    print(f"{result:.6f}")

if __name__ == "__main__":
    main()