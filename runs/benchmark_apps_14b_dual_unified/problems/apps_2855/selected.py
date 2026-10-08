import sys
import numpy as np

def main():
    import sys
    import numpy as np
    
    def read_input():
        import sys
        data = sys.stdin.read().split()
        N = int(data[0])
        M = int(data[1])
        edges = []
        index = 2
        for _ in range(M):
            K = int(data[index])
            L = int(data[index + 1])
            edges.append((K, L))
            index += 2
        return N, M, edges
    
    def build_adjacency_matrix(N, edges):
        adj_matrix = np.zeros((N, N))
        for K, L in edges:
            adj_matrix[K][L] = 1
            adj_matrix[L][K] = 1
        return adj_matrix
    
    def calculate_expected_time(adj_matrix, start, end):
        N = adj_matrix.shape[0]
        Q = adj_matrix.copy()
        Q[end, :] = 0
        Q[:, end] = 0
        Q[end, end] = 1
        
        I = np.eye(N)
        N_matrix = np.linalg.inv(I - Q)
        
        b = np.zeros(N)
        b[end] = 1
        
        expected_times = np.dot(N_matrix, b)
        return expected_times[start]
    
    N, M, edges = read_input()
    adj_matrix = build_adjacency_matrix(N, edges)
    expected_time = calculate_expected_time(adj_matrix, 0, N - 1)
    print(f"{expected_time:.6f}")

if __name__ == "__main__":
    main()