import sys
from collections import defaultdict

def expected_time_to_exit(N, M, paths):
    # Create adjacency list for the graph
    graph = defaultdict(list)
    for K, L in paths:
        graph[K].append(L)
        graph[L].append(K)
    
    # Initialize the transition probability matrix P
    P = [[0.0] * N for _ in range(N)]
    for node in range(N):
        neighbors = graph[node]
        num_neighbors = len(neighbors)
        for neighbor in neighbors:
            P[node][neighbor] = 1.0 / num_neighbors
    
    # Initialize the expected time matrix E
    E = [[0.0] * N for _ in range(N)]
    
    # Calculate expected times using the formula
    for i in range(N):
        for j in range(N):
            if i != j:
                E[i][j] = 1 + sum(P[i][k] * E[k][j] for k in range(N) if k != j)
            else:
                E[i][j] = 0
    
    # Iterate to solve the system of equations
    for _ in range(1000):  # A large number of iterations to ensure convergence
        for i in range(N):
            for j in range(N):
                if i != j:
                    E[i][j] = 1 + sum(P[i][k] * E[k][j] for k in range(N) if k != j)
    
    # The expected time to exit from clearing 0 is E[0][N-1]
    return E[0][N-1]

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