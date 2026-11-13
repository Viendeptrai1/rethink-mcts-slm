import sys
from fractions import Fraction

def get_out_time(N, M, paths):
    # Build the graph
    graph = [[] for _ in range(N)]
    for K, L in paths:
        graph[K].append(L)
        graph[L].append(K)
    
    # Initialize distances and visited arrays
    dist = [float('inf')] * N
    dist[0] = 0
    visited = [False] * N
    
    # Use BFS to calculate expected time
    queue = [(0, Fraction(1))]
    while queue:
        node, prob = queue.pop(0)
        if visited[node]:
            continue
        visited[node] = True
        
        for neighbor in graph[node]:
            new_prob = prob / len(graph[node])
            if dist[node] + 1 < dist[neighbor]:
                dist[neighbor] = dist[node] + 1
                queue.append((neighbor, new_prob))
            elif dist[node] + 1 == dist[neighbor]:
                dist[neighbor] += new_prob
    
    return float(dist[N-1])

# Main function to read input and print output
if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    M = int(data[index + 1])
    index += 2
    
    paths = []
    for _ in range(M):
        K = int(data[index])
        L = int(data[index + 1])
        index += 2
        paths.append((K, L))
    
    result = get_out_time(N, M, paths)
    print(result)