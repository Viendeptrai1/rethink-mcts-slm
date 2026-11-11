import sys
from collections import defaultdict, deque

def max_flow(source, sink, graph):
    def bfs(parent):
        visited = [False] * len(graph)
        queue = deque([source])
        visited[source] = True
        while queue:
            u = queue.popleft()
            for ind, val in enumerate(graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == sink:
                        return True
        return False

    parent = [-1] * len(graph)
    max_flow = 0
    while bfs(parent):
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
        max_flow += path_flow
    return max_flow

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    b = list(map(int, data[n+1:2*n+1]))
    
    if n < 2:
        print(0)
        return
    
    # Create a graph
    graph = [[0] * (2*n + 2) for _ in range(2*n + 2)]
    source = 2*n
    sink = 2*n + 1
    
    # Connect source to all students
    for i in range(n):
        graph[source][i] = 1
    
    # Connect students to sink
    for i in range(n):
        graph[i][n+i] = 1
    
    # Connect students to other students based on compatibility
    for i in range(n):
        for j in range(i+1, n):
            if a[i] & a[j] == a[i] or a[i] & a[j] == a[j]:
                graph[i][n+j] = 1
                graph[j][n+i] = 1
    
    # Calculate maximum flow
    flow = max_flow(source, sink, graph)
    
    # If flow is less than n-1, no valid group exists
    if flow < n - 1:
        print(0)
    else:
        # Find the maximum sum of skill levels in a valid group
        max_sum = 0
        for i in range(n):
            if graph[source][i] == 0:
                max_sum += b[i]
        print(max_sum)

if __name__ == "__main__":
    main()