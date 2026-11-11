import sys
from collections import deque

def max_flow(source, sink, graph):
    n = len(graph)
    parent = [-1] * n
    max_flow_value = 0
    
    while True:
        visited = [False] * n
        queue = deque([source])
        visited[source] = True
        
        while queue:
            u = queue.popleft()
            for v in range(n):
                if not visited[v] and graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
        
        if not visited[sink]:
            break
        
        path_flow = float('Inf')
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
        
        max_flow_value += path_flow
    
    return max_flow_value

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:N+2]))
    B = list(map(int, data[N+2:2*N+2]))
    
    # Create a graph with N+2 nodes: 0 (source), N+1 (sink), and N towns and N heroes
    graph = [[0] * (2 * N + 2) for _ in range(2 * N + 2)]
    
    # Connect source to each hero with capacity B_i
    for i in range(N):
        graph[0][i + 1] = B[i]
    
    # Connect each hero to the corresponding towns with capacity A_i
    for i in range(N):
        graph[i + 1][N + 1 + i] = A[i]
        graph[i + 1][N + 2 + i] = A[i + 1]
    
    # Connect each town to the sink with capacity A_i
    for i in range(N + 1):
        graph[N + 1 + i][2 * N + 1] = A[i]
    
    # Calculate the maximum flow from source to sink
    result = max_flow(0, 2 * N + 1, graph)
    
    print(result)

if __name__ == "__main__":
    main()